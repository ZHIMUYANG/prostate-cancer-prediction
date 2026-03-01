#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
训练额外生存树模型用于前列腺癌骨转移生存预测
"""
import pandas as pd
import joblib
import numpy as np
from sksurv.ensemble import ExtraSurvivalTrees
from sksurv.util import Surv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os


def train_model():
    print("=" * 60)
    print("🚀 开始训练额外生存树模型")
    print("=" * 60)
    
    # 加载数据
    print("📊 加载数据...")
    df = pd.read_csv('data.csv')
    print(f"✅ 数据加载成功！样本量: {df.shape[0]}")
    
    # 准备特征和目标
    features = ['PSA', 'combine_metastasis', 'Age', 'T_stage', 'N_stage', 'Gleason']
    X = df[features].copy()
    y = Surv.from_dataframe('event', 'time', df)
    
    print(f"📋 特征: {features}")
    print(f"📋 目标变量: event={y['event'].mean():.2%} 死亡率")
    
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y['event']
    )
    
    print(f"✅ 数据划分完成 - 训练集: {X_train.shape[0]}, 测试集: {X_test.shape[0]}")
    
    # 训练ExtraSurvivalTrees模型
    print("\n🧠 训练ExtraSurvivalTrees模型...")
    model = ExtraSurvivalTrees(
        n_estimators=200,
        max_depth=6,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    print("✅ 模型训练完成！")
    
    # 评估模型
    print("\n📈 评估模型...")
    risk_scores = model.predict(X_test)
    
    from sksurv.metrics import concordance_index_censored
    c_index = concordance_index_censored(
        y_test['event'],
        y_test['time'],
        risk_scores
    )[0]
    
    print(f"✅ C-index: {c_index:.4f}")
    
    # 保存模型
    model_filename = 'extra_survival_trees_model.pkl'
    joblib.dump(model, model_filename)
    print(f"💾 模型已保存至: {model_filename}")
    
    # 保存模型信息
    model_info = {
        'model_type': 'ExtraSurvivalTrees',
        'features': features,
        'n_estimators': 200,
        'max_depth': 6,
        'min_samples_split': 10,
        'min_samples_leaf': 5,
        'c_index': c_index,
        'training_samples': X_train.shape[0],
        'test_samples': X_test.shape[0]
    }
    
    import json
    with open('model_info.json', 'w', encoding='utf-8') as f:
        json.dump(model_info, f, indent=2, ensure_ascii=False)
    
    print(f"💾 模型信息已保存至: model_info.json")
    print("\n" + "=" * 60)
    print("🎉 模型训练完成！")
    print("=" * 60)
    
    return model, model_info


if __name__ == "__main__":
    model, info = train_model()
