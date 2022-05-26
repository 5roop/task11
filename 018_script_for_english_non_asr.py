# %%
from utils import example_eval_config, example_train_config, train_model, eval_model

# %% [markdown]
# # 1: Gender


# %%
model_name = 'facebook/wav2vec2-large'
results_file = "018_results.jsonl"
results = []


# %%

for clip in [-1, 2]:
    train_config = {
        "model_name_or_path": model_name,
        "TASK": "NEW_GENDER_2s" if clip == 2 else "NEW_GENDER",
        "NUM_EPOCH": 2,
        "data_files": {
            "train": "001_gender_train.csv",
            "validation": "001_gender_dev.csv",
        },
        "clip_seconds": clip,
        "output_column": "Speaker_gender",
    }
    OUTPUT_DIR = train_model(train_config)
    from pathlib import Path

    seed = (
        "models/"
        + train_config.get("model_name_or_path").replace("/", "_")
        + "_"
        + train_config.get("TASK") + "_"
    )
    path = Path(seed)
    OUTPUT_DIR = list(path.rglob("checkpoint*"))[0].absolute().__str__()

    for split in "dev test".split():
        config = {
            "output_column": "Speaker_gender",
            "model_name_or_path": OUTPUT_DIR,
            "eval_file": f"001_gender_{split}.csv",
            "clip_seconds": clip,
            "train_config": train_config,
        }
        try:
            y_true, y_pred = eval_model(config)

            results.append({**config, "y_true": y_true, "y_pred": y_pred})

            import pandas as pd
            df = pd.DataFrame(data=results)
            try:
                df_old = pd.read_json(results_file, orient="records", lines=True)
                df = pd.concat([df, df_old])
            except:
                pass
            df.to_json(results_file, orient="records", lines=True)
        except:
            pass


# # %% [markdown]
# # # 2: speaker ID

# # %%

for clip in [-1, 2]:
    train_config = {
        "model_name_or_path": model_name,
        "TASK": "NEW_SPEAKER_ID_2s" if clip == 2 else "NEW_SPEAKER_ID",
        "NUM_EPOCH": 2,
        "data_files": {
            "train": "003_speaker_id_train_for_datasets.csv",
            "validation": "003_speaker_id_test_for_datasets.csv",
        },
        "clip_seconds": clip,
        "output_column": "Speaker_name",
    }

    OUTPUT_DIR = train_model(train_config)
    from pathlib import Path

    seed = (
        "models/"
        + train_config.get("model_name_or_path").replace("/", "_")
        + "_"
        + train_config.get("TASK") + "_"
    )
    path = Path(seed)
    OUTPUT_DIR = list(path.rglob("checkpoint*"))[0].absolute().__str__()
    for split in "dev test".split():
        config = {
            "output_column": "Speaker_name",
            "model_name_or_path": OUTPUT_DIR,
            "eval_file": f"003_speaker_id_{split}_for_datasets.csv",
            "clip_seconds": clip,
            "train_config": train_config,
        }
        try:

            y_true, y_pred = eval_model(config)

            results.append({**config, "y_true": y_true, "y_pred": y_pred})

            # %%
            import pandas as pd
            df = pd.DataFrame(data=results)
            try:
                df_old = pd.read_json(results_file, orient="records", lines=True)
                df = pd.concat([df, df_old])
            except:
                pass
            df.to_json(results_file, orient="records", lines=True)
        except:
            pass
