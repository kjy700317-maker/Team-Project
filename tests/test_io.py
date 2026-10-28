"""F1 io.py — 작은 합성 자료로 읽기·검증·쓰기 확인. 원자료·기준 CSV는 쓰지 않는다(회귀 테스트는 F3)."""
import pandas as pd
import pytest

from utils.tension import io as tio

HEADER = "사건ID,date,요소,묶음,S,사건명"
GOOD_ROWS = [
    "A2-0002,2010-02-01,A2,핵·미사일,5.5,발사 둘",
    "A2-0001,2010-02-01,A2,핵·미사일,4.0,발사 하나",
    "E5-0001,2010-01-05,E5,북러 밀착,0,회담",
]
TYPE4_HEADER = "사건ID,date,요소,S,사건명,판정유형,4거유형,봉수원뜻,판정근거(팀 요약 원문 문구),비고"


def _write(path, lines, bom=False):
    text = "\n".join(lines) + "\n"
    path.write_bytes((b"\xef\xbb\xbf" if bom else b"") + text.encode("utf-8"))
    return path


def test_bom_and_no_bom_read_same(tmp_path):
    a, _ = tio.load_events(_write(tmp_path / "bom.csv", [HEADER] + GOOD_ROWS, bom=True))
    b, _ = tio.load_events(_write(tmp_path / "nobom.csv", [HEADER] + GOOD_ROWS, bom=False))
    pd.testing.assert_frame_equal(a, b)
    assert list(a.columns) == list(tio.EVENT_COLUMNS)


@pytest.mark.parametrize("header", [
    "date,사건ID,요소,묶음,S,사건명",   # 순서 다름
    "사건ID,date,요소,묶음,S",          # 열 빠짐
])
def test_column_mismatch_raises(tmp_path, header):
    rows = [",".join(r.split(",")[: len(header.split(","))]) for r in GOOD_ROWS]
    with pytest.raises(ValueError):
        tio.load_events(_write(tmp_path / "bad.csv", [header] + rows))


def test_invalid_rows_excluded_with_reason(tmp_path):
    bad = [
        "A2-0010,2010/03/01,A2,핵·미사일,3.0,날짜 형식",
        "A2-0011,2010-03-02,A2,핵·미사일,,S 빈칸",
        "A2-0012,2010-03-03,A2,없는 묶음,3.0,모르는 묶음",
        ",2010-03-04,A2,핵·미사일,3.0,빈 사건ID",
    ]
    ev, exc = tio.load_events(_write(tmp_path / "ev.csv", [HEADER] + GOOD_ROWS + bad))
    assert len(ev) == 3
    assert list(exc.columns) == list(tio.EXCLUDED_COLUMNS)
    reasons = dict(zip(exc["사건명"], exc["사유"]))
    assert reasons == {
        "날짜 형식": "날짜 형식",
        "S 빈칸": "S 숫자 아님",
        "모르는 묶음": "묶음 모름: 없는 묶음",
        "빈 사건ID": "빈칸: 사건ID",
    }
    assert exc.loc[exc["사건명"] == "날짜 형식", "date"].iloc[0] == "2010/03/01"   # 원래 문자열 그대로
    assert (ev.loc[ev["사건ID"] == "E5-0001", "S"] == 0.0).all()                  # S = 0은 정상 행


def test_duplicates(tmp_path):
    ev, exc = tio.load_events(_write(tmp_path / "dup.csv", [HEADER] + GOOD_ROWS + [GOOD_ROWS[0]]))
    assert len(ev) == 3
    assert exc["사유"].tolist() == ["중복 행"] and exc["사건ID"].tolist() == ["A2-0002"]
    clash = GOOD_ROWS[0].replace("5.5", "6.0")
    with pytest.raises(ValueError):
        tio.load_events(_write(tmp_path / "clash.csv", [HEADER] + GOOD_ROWS + [clash]))


def test_sorted_and_dtypes(tmp_path):
    ev, _ = tio.load_events(_write(tmp_path / "ev.csv", [HEADER] + GOOD_ROWS))
    assert ev["사건ID"].tolist() == ["E5-0001", "A2-0001", "A2-0002"]
    assert pd.api.types.is_datetime64_dtype(ev["date"])
    assert ev["S"].dtype == "float64"
    assert ev.index.tolist() == [0, 1, 2]


def _type4(tmp_path, rows):
    return _write(tmp_path / "type4.csv", [TYPE4_HEADER] + rows)


T4_ROWS = [
    "A7-0098,2010-03-26,A7,7.2,Cheonan,사망·침몰,Y,교전(5거),\"sank, explosion\",",
    "A7-0095,2010-01-27,A7,6.45,Artillery,일방 사격, n ,경계 접근(3거),fired,",
]


def test_type4_load_and_ids(tmp_path):
    t = tio.load_type4_table(_type4(tmp_path, T4_ROWS))
    assert list(t.columns) == list(tio.TYPE4_COLUMNS)
    assert t["4거유형"].tolist() == ["Y", "N"]
    assert pd.api.types.is_datetime64_dtype(t["date"])
    assert tio.type4_event_ids(t) == frozenset({"A7-0098"})


def test_type4_bad_flag_raises(tmp_path):
    with pytest.raises(ValueError):
        tio.load_type4_table(_type4(tmp_path, [T4_ROWS[0].replace(",Y,", ",예,")]))


def test_type4_duplicate_id_raises(tmp_path):
    with pytest.raises(ValueError):
        tio.load_type4_table(_type4(tmp_path, [T4_ROWS[0], T4_ROWS[0]]))


def test_type4_against_events(tmp_path):
    ev_lines = [HEADER, "A7-0098,2010-03-27,A7,물리 충돌,7.2,Cheonan"]
    ev, _ = tio.load_events(_write(tmp_path / "ev.csv", ev_lines))
    t = tio.load_type4_table(_type4(tmp_path, T4_ROWS))
    prob = tio.check_type4_against_events(t, ev)
    assert list(prob.columns) == ["사건ID", "문제"]
    got = dict(zip(prob["사건ID"], prob["문제"]))
    assert got == {
        "A7-0098": "날짜 다름(판정표 2010-03-26, 사건표 2010-03-27)",
        "A7-0095": "사건표에 없음",
    }


def test_write_csv_bom_lf_roundtrip(tmp_path):
    df = pd.DataFrame({"사건ID": ["A2-0001", "A2-0002"], "S": [4.0, 0.5], "사건명": ["발사", "가운뎃점·"]})
    path = tmp_path / "sub" / "out.csv"
    tio.write_csv(df, path)
    data = path.read_bytes()
    assert data.startswith(b"\xef\xbb\xbf")
    assert b"\r\n" not in data
    pd.testing.assert_frame_equal(tio.read_csv_kr(path), df)
