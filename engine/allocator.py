import pandas as pd
import xgboost as xgb

class CapitalAllocator:
    def __init__(self, model_path, pods):
        self.pods = pods
        self.model = xgb.XGBRegressor()
        self.model.load_model(model_path)

    def collect_features(self):
        return pd.DataFrame([pod.get_features() for pod in self.pods])

    def reallocate(self):
        df = self.collect_features()
        preds = self.model.predict(df.drop(['name'], axis=1))
        preds = preds.clip(0, None)
        weights = preds / preds.sum()
        total_capital = sum(p.capital for p in self.pods)

        for i, pod in enumerate(self.pods):
            new_capital = total_capital * weights[i]
            pod.capital = new_capital
            print(f"[Allocator] Allocated ${new_capital:.2f} to {pod.name}")
