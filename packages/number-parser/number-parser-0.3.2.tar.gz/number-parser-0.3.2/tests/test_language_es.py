import pytest
from number_parser import parse, parse_number
from tests import HUNDREDS_DIRECTORY, PERMUTATION_DIRECTORY
from tests import _test_files
LANG = 'es'


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("veintiséis", 26),
        ("treinta y una", 31),
        ("ciento uno", 101),
        ("Doscientos cincuenta y seis", 256),
        ("trescientos dos", 302),
        ("trescientas cuarenta y dos", 342),
        ("cuatrocientos veinticuatro", 424),
        ("seiscientos sesenta y seis", 666),
        ("Cien mil", 100000),
        ("un millón cuatrocientos treinta y dos mil quinientos veinticuatro", 1_432_524),
        ("mil millones", 1_000_000_000),
        ("millardo", 1_000_000_000),
        ("Dos mil ciento cuarenta y siete millones cuatrocientos ochenta \
            y tres mil seiscientos cuarenta y siete", 2_147_483_647),
        ("tres mil millones veinticuatro", 3_000_000_024),
        ("tres mil veintitrés millones mil cuatrocientos treinta y dos", 3_023_001_432),
        ("cinco billones trescientos veinte millones", 5_000_320_000_000),
        ("cinco trillones setecientos sesenta y cuatro mil seiscientos siete billones \
        quinientos mil millones treinta y uno", 5_764_607_500_000_000_031),
        ("cuatrillón", 10**24),
        ("Gúgol", 10**100),
        ("centillón", 10**600),
    ]
)
def test_parse_number(expected, test_input):
    assert parse_number(test_input, LANG) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("Hay tres gallinas y veintitrés patos", "Hay 3 gallinas y 23 patos"),
        ("En España viven cuarenta y seis millones novecientas cuarenta mil personas",
         "En España viven 46940000 personas"),
        ("dos y dos son cuatro cuatro y dos son seis seis y dos son ocho y ocho dieciséis",
         "2 y 2 son 4 4 y 2 son 6 6 y 2 son 8 y 8 16"),
        ("doscientos cincuenta y doscientos treinta y uno y doce", "250 y 231 y 12"),
        ('Avisté tres y luego nos fuimos.', 'Avisté 3 y luego nos fuimos.')
    ]
)
def test_parse(expected, test_input):
    assert parse(test_input, LANG) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("uno, dos, tres,", "1, 2, 3,"),
        ("uno , dos , tres ,", "1 , 2 , 3 ,"),
        ("cincuenta y uno . sesenta y dos . setenta y tres .", "51 . 62 . 73 ."),
        ("ciento cinco. dos mil ocho .", "105. 2008 ."),
    ]
)
def test_parse_separators_and_spacing(expected, test_input):
    assert parse(test_input, LANG) == expected


def test_parse_number_till_hundred():
    _test_files(HUNDREDS_DIRECTORY, LANG)


def test_parse_number_permutations():
    _test_files(PERMUTATION_DIRECTORY, LANG)
