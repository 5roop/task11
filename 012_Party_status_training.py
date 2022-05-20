from utils import example_eval_config, example_train_config, train_model, eval_model


results = []


# %%

for clip in [-1]:
    train_config = {
        'model_name_or_path': 'facebook/wav2vec2-large-slavic-voxpopuli-v2',
        'TASK': 'PARTY_STATUS_2s' if clip==2 else "PARTY_STATUS",
        'NUM_EPOCH': 15,
        'data_files': {
            'train': '012_train.csv',
            'validation': '012_dev.csv'
            },
        "clip_seconds": clip,
        "output_column": "Party_status"
    }

    # OUTPUT_DIR = train_model(train_config)
    print(train_config)
    # print(OUTPUT_DIR)
    for split in "dev test".split():
        config = {
            "output_column": "Party_status",
            "model_name_or_path": "/home/peterr/macocu/task11/models/facebook_wav2vec2-large-slavic-voxpopuli-v2_PARTY_STATUS_/checkpoint-4680",
            "eval_file": f"012_{split}.csv",
            "clip_seconds": clip,
            "train_config": train_config
        }
        y_true, y_pred = eval_model(config)

        results.append({**config, "y_true": y_true, "y_pred": y_pred})


        import pandas as pd
        df = pd.DataFrame(data=results)
        df.to_json("012_results.jsonl", orient="records", lines=True)