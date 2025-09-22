"""."""

from math import prod

TYPES: tuple[str, ...] = (
    "normal",
    "fire",
    "water",
    "electric",
    "grass",
    "ice",
    "fighting",
    "poison",
    "ground",
    "flying",
    "psychic",
    "bug",
    "rock",
    "ghost",
    "dragon",
    "dark",
    "steel",
    "fairy",
)

TYPE_CHART: dict[str, dict[str, int | float]] = {
    "normal": {
        "normal": 1,
        "fire": 1,
        "water": 1,
        "electric": 1,
        "grass": 1,
        "ice": 1,
        "fighting": 1,
        "poison": 1,
        "ground": 1,
        "flying": 1,
        "psychic": 1,
        "bug": 1,
        "rock": 0.5,
        "ghost": 0,
        "dragon": 1,
        "dark": 1,
        "steel": 0.5,
        "fairy": 1,
    },
    "fire": {
        "normal": 1,
        "fire": 0.5,
        "water": 0.5,
        "electric": 1,
        "grass": 2,
        "ice": 2,
        "fighting": 1,
        "poison": 1,
        "ground": 1,
        "flying": 1,
        "psychic": 1,
        "bug": 2,
        "rock": 0.5,
        "ghost": 1,
        "dragon": 0.5,
        "dark": 1,
        "steel": 2,
        "fairy": 1,
    },
    "water": {
        "normal": 1,
        "fire": 2,
        "water": 0.5,
        "electric": 1,
        "grass": 0.5,
        "ice": 1,
        "fighting": 1,
        "poison": 1,
        "ground": 2,
        "flying": 1,
        "psychic": 1,
        "bug": 1,
        "rock": 2,
        "ghost": 1,
        "dragon": 0.5,
        "dark": 1,
        "steel": 1,
        "fairy": 1,
    },
    "electric": {
        "normal": 1,
        "fire": 1,
        "water": 2,
        "electric": 0.5,
        "grass": 0.5,
        "ice": 1,
        "fighting": 1,
        "poison": 1,
        "ground": 0,
        "flying": 2,
        "psychic": 1,
        "bug": 1,
        "rock": 1,
        "ghost": 1,
        "dragon": 0.5,
        "dark": 1,
        "steel": 1,
        "fairy": 1,
    },
    "grass": {
        "normal": 1,
        "fire": 0.5,
        "water": 2,
        "electric": 1,
        "grass": 0.5,
        "ice": 1,
        "fighting": 1,
        "poison": 0.5,
        "ground": 2,
        "flying": 0.5,
        "psychic": 1,
        "bug": 0.5,
        "rock": 2,
        "ghost": 1,
        "dragon": 0.5,
        "dark": 1,
        "steel": 0.5,
        "fairy": 1,
    },
    "ice": {
        "normal": 1,
        "fire": 0.5,
        "water": 0.5,
        "electric": 1,
        "grass": 2,
        "ice": 0.5,
        "fighting": 1,
        "poison": 1,
        "ground": 2,
        "flying": 2,
        "psychic": 1,
        "bug": 1,
        "rock": 1,
        "ghost": 1,
        "dragon": 2,
        "dark": 1,
        "steel": 0.5,
        "fairy": 1,
    },
    "fighting": {
        "normal": 2,
        "fire": 1,
        "water": 1,
        "electric": 1,
        "grass": 1,
        "ice": 2,
        "fighting": 1,
        "poison": 0.5,
        "ground": 1,
        "flying": 0.5,
        "psychic": 0.5,
        "bug": 0.5,
        "rock": 2,
        "ghost": 0,
        "dragon": 1,
        "dark": 2,
        "steel": 2,
        "fairy": 0.5,
    },
    "poison": {
        "normal": 1,
        "fire": 1,
        "water": 1,
        "electric": 1,
        "grass": 2,
        "ice": 1,
        "fighting": 1,
        "poison": 0.5,
        "ground": 0.5,
        "flying": 1,
        "psychic": 1,
        "bug": 1,
        "rock": 0.5,
        "ghost": 0.5,
        "dragon": 1,
        "dark": 1,
        "steel": 0,
        "fairy": 2,
    },
    "ground": {
        "normal": 1,
        "fire": 2,
        "water": 1,
        "electric": 2,
        "grass": 0.5,
        "ice": 1,
        "fighting": 1,
        "poison": 2,
        "ground": 1,
        "flying": 0,
        "psychic": 1,
        "bug": 0.5,
        "rock": 2,
        "ghost": 1,
        "dragon": 1,
        "dark": 1,
        "steel": 2,
        "fairy": 1,
    },
    "flying": {
        "normal": 1,
        "fire": 1,
        "water": 1,
        "electric": 0.5,
        "grass": 2,
        "ice": 1,
        "fighting": 2,
        "poison": 1,
        "ground": 1,
        "flying": 1,
        "psychic": 1,
        "bug": 2,
        "rock": 0.5,
        "ghost": 1,
        "dragon": 1,
        "dark": 1,
        "steel": 0.5,
        "fairy": 1,
    },
    "psychic": {
        "normal": 1,
        "fire": 1,
        "water": 1,
        "electric": 1,
        "grass": 1,
        "ice": 1,
        "fighting": 2,
        "poison": 2,
        "ground": 1,
        "flying": 1,
        "psychic": 0.5,
        "bug": 1,
        "rock": 1,
        "ghost": 1,
        "dragon": 1,
        "dark": 0,
        "steel": 0.5,
        "fairy": 1,
    },
    "bug": {
        "normal": 1,
        "fire": 0.5,
        "water": 1,
        "electric": 1,
        "grass": 2,
        "ice": 1,
        "fighting": 0.5,
        "poison": 0.5,
        "ground": 1,
        "flying": 0.5,
        "psychic": 2,
        "bug": 1,
        "rock": 1,
        "ghost": 0.5,
        "dragon": 1,
        "dark": 2,
        "steel": 0.5,
        "fairy": 0.5,
    },
    "rock": {
        "normal": 1,
        "fire": 2,
        "water": 1,
        "electric": 1,
        "grass": 1,
        "ice": 2,
        "fighting": 0.5,
        "poison": 1,
        "ground": 0.5,
        "flying": 2,
        "psychic": 1,
        "bug": 2,
        "rock": 1,
        "ghost": 1,
        "dragon": 1,
        "dark": 1,
        "steel": 0.5,
        "fairy": 1,
    },
    "ghost": {
        "normal": 0,
        "fire": 1,
        "water": 1,
        "electric": 1,
        "grass": 1,
        "ice": 1,
        "fighting": 1,
        "poison": 1,
        "ground": 1,
        "flying": 1,
        "psychic": 2,
        "bug": 1,
        "rock": 1,
        "ghost": 2,
        "dragon": 1,
        "dark": 0.5,
        "steel": 1,
        "fairy": 1,
    },
    "dragon": {
        "normal": 1,
        "fire": 1,
        "water": 1,
        "electric": 1,
        "grass": 1,
        "ice": 1,
        "fighting": 1,
        "poison": 1,
        "ground": 1,
        "flying": 1,
        "psychic": 1,
        "bug": 1,
        "rock": 1,
        "ghost": 1,
        "dragon": 2,
        "dark": 1,
        "steel": 0.5,
        "fairy": 0,
    },
    "dark": {
        "normal": 1,
        "fire": 1,
        "water": 1,
        "electric": 1,
        "grass": 1,
        "ice": 1,
        "fighting": 0.5,
        "poison": 1,
        "ground": 1,
        "flying": 1,
        "psychic": 2,
        "bug": 1,
        "rock": 1,
        "ghost": 2,
        "dragon": 1,
        "dark": 0.5,
        "steel": 1,
        "fairy": 0.5,
    },
    "steel": {
        "normal": 1,
        "fire": 0.5,
        "water": 0.5,
        "electric": 0.5,
        "grass": 1,
        "ice": 2,
        "fighting": 1,
        "poison": 1,
        "ground": 1,
        "flying": 1,
        "psychic": 1,
        "bug": 1,
        "rock": 2,
        "ghost": 1,
        "dragon": 0.5,
        "dark": 1,
        "steel": 0.5,
        "fairy": 2,
    },
    "fairy": {
        "normal": 1,
        "fire": 0.5,
        "water": 1,
        "electric": 1,
        "grass": 1,
        "ice": 1,
        "fighting": 2,
        "poison": 0.5,
        "ground": 1,
        "flying": 1,
        "psychic": 1,
        "bug": 1,
        "rock": 1,
        "ghost": 1,
        "dragon": 2,
        "dark": 2,
        "steel": 0.5,
        "fairy": 1,
    },
}

# region: TYPE_CONSTANTS
NORMAL_NORMAL = frozenset(("normal", "normal"))
NORMAL_FIRE = frozenset(("normal", "fire"))
NORMAL_WATER = frozenset(("normal", "water"))
NORMAL_ELECTRIC = frozenset(("normal", "electric"))
NORMAL_GRASS = frozenset(("normal", "grass"))
NORMAL_ICE = frozenset(("normal", "ice"))
NORMAL_FIGHTING = frozenset(("normal", "fighting"))
NORMAL_POISON = frozenset(("normal", "poison"))
NORMAL_GROUND = frozenset(("normal", "ground"))
NORMAL_FLYING = frozenset(("normal", "flying"))
NORMAL_PSYCHIC = frozenset(("normal", "psychic"))
NORMAL_BUG = frozenset(("normal", "bug"))
NORMAL_ROCK = frozenset(("normal", "rock"))
NORMAL_GHOST = frozenset(("normal", "ghost"))
NORMAL_DRAGON = frozenset(("normal", "dragon"))
NORMAL_DARK = frozenset(("normal", "dark"))
NORMAL_STEEL = frozenset(("normal", "steel"))
NORMAL_FAIRY = frozenset(("normal", "fairy"))

FIRE_FIRE = frozenset(("fire", "fire"))
FIRE_WATER = frozenset(("fire", "water"))
FIRE_ELECTRIC = frozenset(("fire", "electric"))
FIRE_GRASS = frozenset(("fire", "grass"))
FIRE_ICE = frozenset(("fire", "ice"))
FIRE_FIGHTING = frozenset(("fire", "fighting"))
FIRE_POISON = frozenset(("fire", "poison"))
FIRE_GROUND = frozenset(("fire", "ground"))
FIRE_FLYING = frozenset(("fire", "flying"))
FIRE_PSYCHIC = frozenset(("fire", "psychic"))
FIRE_BUG = frozenset(("fire", "bug"))
FIRE_ROCK = frozenset(("fire", "rock"))
FIRE_GHOST = frozenset(("fire", "ghost"))
FIRE_DRAGON = frozenset(("fire", "dragon"))
FIRE_DARK = frozenset(("fire", "dark"))
FIRE_STEEL = frozenset(("fire", "steel"))
FIRE_FAIRY = frozenset(("fire", "fairy"))

WATER_WATER = frozenset(("water", "water"))
WATER_ELECTRIC = frozenset(("water", "electric"))
WATER_GRASS = frozenset(("water", "grass"))
WATER_ICE = frozenset(("water", "ice"))
WATER_FIGHTING = frozenset(("water", "fighting"))
WATER_POISON = frozenset(("water", "poison"))
WATER_GROUND = frozenset(("water", "ground"))
WATER_FLYING = frozenset(("water", "flying"))
WATER_PSYCHIC = frozenset(("water", "psychic"))
WATER_BUG = frozenset(("water", "bug"))
WATER_ROCK = frozenset(("water", "rock"))
WATER_GHOST = frozenset(("water", "ghost"))
WATER_DRAGON = frozenset(("water", "dragon"))
WATER_DARK = frozenset(("water", "dark"))
WATER_STEEL = frozenset(("water", "steel"))
WATER_FAIRY = frozenset(("water", "fairy"))

ELECTRIC_ELECTRIC = frozenset(("electric", "electric"))
ELECTRIC_GRASS = frozenset(("electric", "grass"))
ELECTRIC_ICE = frozenset(("electric", "ice"))
ELECTRIC_FIGHTING = frozenset(("electric", "fighting"))
ELECTRIC_POISON = frozenset(("electric", "poison"))
ELECTRIC_GROUND = frozenset(("electric", "ground"))
ELECTRIC_FLYING = frozenset(("electric", "flying"))
ELECTRIC_PSYCHIC = frozenset(("electric", "psychic"))
ELECTRIC_BUG = frozenset(("electric", "bug"))
ELECTRIC_ROCK = frozenset(("electric", "rock"))
ELECTRIC_GHOST = frozenset(("electric", "ghost"))
ELECTRIC_DRAGON = frozenset(("electric", "dragon"))
ELECTRIC_DARK = frozenset(("electric", "dark"))
ELECTRIC_STEEL = frozenset(("electric", "steel"))
ELECTRIC_FAIRY = frozenset(("electric", "fairy"))

GRASS_GRASS = frozenset(("grass", "grass"))
GRASS_ICE = frozenset(("grass", "ice"))
GRASS_FIGHTING = frozenset(("grass", "fighting"))
GRASS_POISON = frozenset(("grass", "poison"))
GRASS_GROUND = frozenset(("grass", "ground"))
GRASS_FLYING = frozenset(("grass", "flying"))
GRASS_PSYCHIC = frozenset(("grass", "psychic"))
GRASS_BUG = frozenset(("grass", "bug"))
GRASS_ROCK = frozenset(("grass", "rock"))
GRASS_GHOST = frozenset(("grass", "ghost"))
GRASS_DRAGON = frozenset(("grass", "dragon"))
GRASS_DARK = frozenset(("grass", "dark"))
GRASS_STEEL = frozenset(("grass", "steel"))
GRASS_FAIRY = frozenset(("grass", "fairy"))

ICE_ICE = frozenset(("ice", "ice"))
ICE_FIGHTING = frozenset(("ice", "fighting"))
ICE_POISON = frozenset(("ice", "poison"))
ICE_GROUND = frozenset(("ice", "ground"))
ICE_FLYING = frozenset(("ice", "flying"))
ICE_PSYCHIC = frozenset(("ice", "psychic"))
ICE_BUG = frozenset(("ice", "bug"))
ICE_ROCK = frozenset(("ice", "rock"))
ICE_GHOST = frozenset(("ice", "ghost"))
ICE_DRAGON = frozenset(("ice", "dragon"))
ICE_DARK = frozenset(("ice", "dark"))
ICE_STEEL = frozenset(("ice", "steel"))
ICE_FAIRY = frozenset(("ice", "fairy"))

FIGHTING_FIGHTING = frozenset(("fighting", "fighting"))
FIGHTING_POISON = frozenset(("fighting", "poison"))
FIGHTING_GROUND = frozenset(("fighting", "ground"))
FIGHTING_FLYING = frozenset(("fighting", "flying"))
FIGHTING_PSYCHIC = frozenset(("fighting", "psychic"))
FIGHTING_BUG = frozenset(("fighting", "bug"))
FIGHTING_ROCK = frozenset(("fighting", "rock"))
FIGHTING_GHOST = frozenset(("fighting", "ghost"))
FIGHTING_DRAGON = frozenset(("fighting", "dragon"))
FIGHTING_DARK = frozenset(("fighting", "dark"))
FIGHTING_STEEL = frozenset(("fighting", "steel"))
FIGHTING_FAIRY = frozenset(("fighting", "fairy"))

POISON_POISON = frozenset(("poison", "poison"))
POISON_GROUND = frozenset(("poison", "ground"))
POISON_FLYING = frozenset(("poison", "flying"))
POISON_PSYCHIC = frozenset(("poison", "psychic"))
POISON_BUG = frozenset(("poison", "bug"))
POISON_ROCK = frozenset(("poison", "rock"))
POISON_GHOST = frozenset(("poison", "ghost"))
POISON_DRAGON = frozenset(("poison", "dragon"))
POISON_DARK = frozenset(("poison", "dark"))
POISON_STEEL = frozenset(("poison", "steel"))
POISON_FAIRY = frozenset(("poison", "fairy"))

GROUND_GROUND = frozenset(("ground", "ground"))
GROUND_FLYING = frozenset(("ground", "flying"))
GROUND_PSYCHIC = frozenset(("ground", "psychic"))
GROUND_BUG = frozenset(("ground", "bug"))
GROUND_ROCK = frozenset(("ground", "rock"))
GROUND_GHOST = frozenset(("ground", "ghost"))
GROUND_DRAGON = frozenset(("ground", "dragon"))
GROUND_DARK = frozenset(("ground", "dark"))
GROUND_STEEL = frozenset(("ground", "steel"))
GROUND_FAIRY = frozenset(("ground", "fairy"))

FLYING_FLYING = frozenset(("flying", "flying"))
FLYING_PSYCHIC = frozenset(("flying", "psychic"))
FLYING_BUG = frozenset(("flying", "bug"))
FLYING_ROCK = frozenset(("flying", "rock"))
FLYING_GHOST = frozenset(("flying", "ghost"))
FLYING_DRAGON = frozenset(("flying", "dragon"))
FLYING_DARK = frozenset(("flying", "dark"))
FLYING_STEEL = frozenset(("flying", "steel"))
FLYING_FAIRY = frozenset(("flying", "fairy"))

PSYCHIC_PSYCHIC = frozenset(("psychic", "psychic"))
PSYCHIC_BUG = frozenset(("psychic", "bug"))
PSYCHIC_ROCK = frozenset(("psychic", "rock"))
PSYCHIC_GHOST = frozenset(("psychic", "ghost"))
PSYCHIC_DRAGON = frozenset(("psychic", "dragon"))
PSYCHIC_DARK = frozenset(("psychic", "dark"))
PSYCHIC_STEEL = frozenset(("psychic", "steel"))
PSYCHIC_FAIRY = frozenset(("psychic", "fairy"))

BUG_BUG = frozenset(("bug", "bug"))
BUG_ROCK = frozenset(("bug", "rock"))
BUG_GHOST = frozenset(("bug", "ghost"))
BUG_DRAGON = frozenset(("bug", "dragon"))
BUG_DARK = frozenset(("bug", "dark"))
BUG_STEEL = frozenset(("bug", "steel"))
BUG_FAIRY = frozenset(("bug", "fairy"))

ROCK_ROCK = frozenset(("rock", "rock"))
ROCK_GHOST = frozenset(("rock", "ghost"))
ROCK_DRAGON = frozenset(("rock", "dragon"))
ROCK_DARK = frozenset(("rock", "dark"))
ROCK_STEEL = frozenset(("rock", "steel"))
ROCK_FAIRY = frozenset(("rock", "fairy"))

GHOST_GHOST = frozenset(("ghost", "ghost"))
GHOST_DRAGON = frozenset(("ghost", "dragon"))
GHOST_DARK = frozenset(("ghost", "dark"))
GHOST_STEEL = frozenset(("ghost", "steel"))
GHOST_FAIRY = frozenset(("ghost", "fairy"))

DRAGON_DRAGON = frozenset(("dragon", "dragon"))
DRAGON_DARK = frozenset(("dragon", "dark"))
DRAGON_STEEL = frozenset(("dragon", "steel"))
DRAGON_FAIRY = frozenset(("dragon", "fairy"))

DARK_DARK = frozenset(("dark", "dark"))
DARK_STEEL = frozenset(("dark", "steel"))
DARK_FAIRY = frozenset(("dark", "fairy"))

STEEL_STEEL = frozenset(("steel", "steel"))
STEEL_FAIRY = frozenset(("steel", "fairy"))

FAIRY_FAIRY = frozenset(("fairy", "fairy"))
# endregion

DUAL_TYPES: frozenset[frozenset[str]] = frozenset(frozenset((t1, t2)) for t1 in TYPES for t2 in TYPES)
duals = [frozenset((TYPES[i], TYPES[j])) for i in range(len(TYPES)) for j in range(i, len(TYPES))]
dual_scores = [
    x * 84.99320358985798
    for x in [
        0.06099708268989983,
        0.07609668309797292,
        0.07755098162773733,
        0.07528787581726906,
        0.06697917958709365,
        0.07042041698182097,
        0.06875172446240499,
        0.0694707402033407,
        0.07871372802753264,
        0.07323443566449268,
        0.0734142231474166,
        0.06896843606909984,
        0.07081173266313882,
        0.08114435019846389,
        0.06949257906575437,
        0.07174329343762528,
        0.08051413755887118,
        0.07707333217963225,
        0.07196733599403997,
        0.0822145977462367,
        0.08048466345048298,
        0.08008416541007814,
        0.07670186749098513,
        0.08061798471687527,
        0.07624386645555797,
        0.08776581339080189,
        0.08024170636459432,
        0.07842869458115684,
        0.07642054379060188,
        0.07792274132754143,
        0.08149382555217943,
        0.08108635221014555,
        0.07972598994678298,
        0.08132764024997748,
        0.08290273705547217,
        0.0738765670814289,
        0.08110635890290156,
        0.07508760465680409,
        0.07865085111906754,
        0.07859748991628117,
        0.08329739091634021,
        0.08586540296305616,
        0.08410507231498227,
        0.07687230328350217,
        0.0801906595523224,
        0.07886822172722424,
        0.08264157449142727,
        0.0814419756756884,
        0.07794116333602953,
        0.0849322782015798,
        0.08497007083544503,
        0.06678378352588568,
        0.07200421919651631,
        0.07786109803338916,
        0.07985640838887952,
        0.07850646723260973,
        0.08157617127878836,
        0.08188212837484066,
        0.07501370307342767,
        0.07833342663429348,
        0.07490521478869988,
        0.08075201112892263,
        0.07545277752902801,
        0.07617804292105185,
        0.08276417416423272,
        0.08279844458345843,
        0.058479650323857144,
        0.06882502896388686,
        0.06990635907412243,
        0.0720162836569761,
        0.0751690925656788,
        0.07250924800380361,
        0.06729986899770189,
        0.06367756447029613,
        0.07887237159370081,
        0.07510174996932503,
        0.06778473297611413,
        0.06840617970572468,
        0.08060977514310849,
        0.07258065142641656,
        0.06742960171786011,
        0.07712075551199601,
        0.07309356241777559,
        0.08328799877661246,
        0.07467707845151807,
        0.07190280073272544,
        0.06998267673901543,
        0.0729180612295194,
        0.07779417834499505,
        0.07363459971828158,
        0.07156548921918267,
        0.07870948133566741,
        0.07463488832787037,
        0.06321328111252883,
        0.07674894157543237,
        0.07688275392825408,
        0.07996061595312456,
        0.0798324598502394,
        0.07149471645065407,
        0.07753706634621016,
        0.08252510264731804,
        0.07615511893099207,
        0.0799705242159704,
        0.08384228267601063,
        0.07746595217275272,
        0.060234744856404975,
        0.08264010941333622,
        0.07383745923351437,
        0.07404715678160786,
        0.06839276056828127,
        0.07450480629943806,
        0.0774863885360134,
        0.0749698346445271,
        0.08246788120157773,
        0.08028592588010074,
        0.0766080953530492,
        0.07045358537239108,
        0.08810992765207135,
        0.0769272423378444,
        0.0805176476562979,
        0.07805291628650511,
        0.08218445669214106,
        0.08055778315435881,
        0.07872338504481863,
        0.08777148225173652,
        0.08603398554434964,
        0.07084952962955093,
        0.07216009079421647,
        0.07043408885235967,
        0.07825149419582203,
        0.07807127149925701,
        0.07453908951312235,
        0.0785742841357946,
        0.0877414002549554,
        0.07599463821579963,
        0.06406699776010721,
        0.0709343621377375,
        0.07312945035075082,
        0.07548329195052206,
        0.07054281590450659,
        0.07562311940066314,
        0.0800874072809677,
        0.07677641573068052,
        0.060195549536478946,
        0.07804257315381534,
        0.07538857286678381,
        0.06987853232264757,
        0.0703298589130096,
        0.08238821557889091,
        0.07149056170545819,
        0.06907626168614014,
        0.07761792265398405,
        0.07472088730144642,
        0.07261858900072435,
        0.07997836046033566,
        0.07979248624314776,
        0.06877145970112279,
        0.07811837052886945,
        0.07902191370033665,
        0.08683098360112304,
        0.08386573523321612,
        0.06552424292032369,
        0.07245435691951418,
        0.08577940828226004,
        0.07801175394504743,
        0.06833136120136728,
        0.08403167536389736,
        0.08080831490852695,
        0.07289999294553741,
        0.08771094821357792,
        0.07311026857313073,
    ]
]
dual_score_map = {duals[i]: dual_scores[i] for i in range(len(duals))}

DUAL_TYPE_CHART: dict[frozenset[str], dict[frozenset[str], int | float]] = {
    dual_atk: {
        dual_def: max((prod((TYPE_CHART[atk_type][def_type] for def_type in dual_def)) for atk_type in dual_atk))
        for dual_def in DUAL_TYPES
    }
    for dual_atk in DUAL_TYPES
}

MATCHUPS: dict[str, dict[str, int | float]] = {
    attacker: {
        defender: (TYPE_CHART[attacker][defender] / denominator)
        if (denominator := TYPE_CHART[attacker][defender] + TYPE_CHART[defender][attacker]) != 0
        else 0.5
        for defender in TYPES
    }
    for attacker in TYPES
}

DUAL_MATCHUPS: dict[frozenset[str], dict[frozenset[str], int | float]] = {
    attacker: {
        defender: (DUAL_TYPE_CHART[attacker][defender] / denominator)
        if (denominator := DUAL_TYPE_CHART[attacker][defender] + DUAL_TYPE_CHART[defender][attacker]) != 0
        else 0.5
        for defender in DUAL_TYPES
    }
    for attacker in DUAL_TYPES
}


if __name__ == "__main__":
    np.set_printoptions(linewidth=400)
    print()
    print(f"{dual_score_map=}")
    # print()
    # print(f"{DUAL_TYPE_CHART[FIRE_WATER][FIRE_ELECTRIC]=}")
    # print()
    # print(f"{MATCHUPS['water']['fire']=}")
    # print()
    # print(f"{DUAL_MATCHUPS[FIRE_FIRE][FIRE_FIRE]=}")
    # print(f"{DUAL_MATCHUPS[FIRE_FIRE][FIRE_WATER]=}")
    # print(f"{DUAL_MATCHUPS[FIRE_WATER][FIRE_ELECTRIC]=}")
    print()
