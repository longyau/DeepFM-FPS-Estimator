
# set the path-to-files
TRAIN_FILE = "./data/trainFYP.csv"
TEST_FILE = "./data/testFYP.csv"

SUB_DIR = "./outputFYP"


NUM_SPLITS = 3
RANDOM_SEED = 2017

# types of columns of the dataset dataframe
CATEGORICAL_COLS = [
    # 'ps_ind_02_cat', 'ps_ind_04_cat', 'ps_ind_05_cat',
    # 'ps_car_01_cat', 'ps_car_02_cat', 'ps_car_03_cat',
    # 'ps_car_04_cat', 'ps_car_05_cat', 'ps_car_06_cat',
    # 'ps_car_07_cat', 'ps_car_08_cat', 'ps_car_09_cat',
    # 'ps_car_10_cat', 'ps_car_11_cat',
    "CPU-Part Number","CPU-Codename","CPU-Brand","CPU-Name","CPU-Socket",
    "GPU-Brand","GPU-Direct X","GPU-Name","GPU-Name2","GPU-Power Connector","GPU-Architecture","GPU-Memory Type",
    "GAME-Rec-DX","GAME-Theme","GAME-Min-DX","GAME-Min-CPU0","GAME-Min-CPU1","GAME-Min-GPU1","GAME-Min-GPU0","GAME-Name","GAME-Rec-CPU1","GAME-Min-OS","GAME-Rec-CPU0","GAME-Rec-GPU1","GAME-Rec-GPU0","GAME-Rec-OS","GAME-Genre1","GAME-Genre0","Game-Setting",
]

NUMERIC_COLS = [
    # # binary
    # "ps_ind_06_bin", "ps_ind_07_bin", "ps_ind_08_bin",
    # "ps_ind_09_bin", "ps_ind_10_bin", "ps_ind_11_bin",
    # "ps_ind_12_bin", "ps_ind_13_bin", "ps_ind_16_bin",
    # "ps_ind_17_bin", "ps_ind_18_bin",
    # "ps_calc_15_bin", "ps_calc_16_bin", "ps_calc_17_bin",
    # "ps_calc_18_bin", "ps_calc_19_bin", "ps_calc_20_bin",
    # numeric
    # "ps_reg_01", "ps_reg_02", "ps_reg_03",
    # "ps_car_12", "ps_car_13", "ps_car_14", "ps_car_15",
    "CPU-Score","CPU-Cache L1","CPU-Cache L3","CPU-Cache L2","CPU-Samples","CPU-Process","CPU-Cores","CPU-Clock","CPU-Multi","CPU-Price","CPU-TDP","CPU-Released",
    "GPU-L2 Cache","GPU-Shader Processing Units","GPU-Process","GPU-Samples","GPU-Release Price","GPU-TMUs","GPU-PSU","GPU-ROPs","GPU-Max Power","GPU-Texture Rate","GPU-Memory","GPU-GD RATING","GPU-Core Speed","GPU-Pixel Rate","GPU-Memory Bandwidth","GPU-Shader","GPU-Benchmark","GPU-Memory Speed","GPU-Open GL","GPU-Memory Bus","GPU-Memory",
    "GAME-Rec-Ram","GAME-Release Date2","GAME-Release Date0","GAME-Release Date1","GAME-Min-VRam","GAME-Min-Ram","GAME-Rec-VRam",
    "Res-Height","Res-Width","Ram",
    # feature engineering
    "missing_feat"
    # "ps_car_13_x_ps_reg_03",
]

IGNORE_COLS = [
    "CPU-URL","CPU-Type"
    "GPU-Type","GPU-Website","GPU-BenchmarkURL",
    "GAME-Website","GAME-Type",
    "id","target"
    # "id", "target",
    # "ps_calc_01", "ps_calc_02", "ps_calc_03", "ps_calc_04",
    # "ps_calc_05", "ps_calc_06", "ps_calc_07", "ps_calc_08",
    # "ps_calc_09", "ps_calc_10", "ps_calc_11", "ps_calc_12",
    # "ps_calc_13", "ps_calc_14",
    # "ps_calc_15_bin", "ps_calc_16_bin", "ps_calc_17_bin",
    # "ps_calc_18_bin", "ps_calc_19_bin", "ps_calc_20_bin"
]
