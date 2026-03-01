# 前列腺癌骨转移生存预测系统

基于额外生存树模型的交互式预测平台

## 功能特点

- 训练额外生存树模型
- Web界面输入患者特征
- 实时预测风险分数和生存概率
- 可视化生存曲线
- 提供临床建议

## 安装步骤

### 1. 安装Python依赖

```bash
pip install -r requirements.txt
```

### 2. 训练模型

```bash
python train_model.py
```

训练完成后会生成：
- `extra_survival_trees_model.pkl` - 训练好的模型文件
- `model_info.json` - 模型配置信息

### 3. 启动Web应用

```bash
streamlit run app.py
```

应用将在浏览器中自动打开（默认地址：http://localhost:8501）

## 使用说明

### 输入特征

在Web界面中输入以下患者特征：

1. **PSA** (前列腺特异性抗原)：0-1000 ng/mL
2. **骨转移** (combine_metastasis)：0（无）或 1（有）
3. **年龄**：30-100岁
4. **T分期**：1-4期
5. **N分期**：0（无转移）或 1（有转移）
6. **Gleason评分**：6-10分

### 预测结果

- **风险分数**：数值越高，预后越差
- **风险等级**：低风险、中风险、高风险
- **生存概率**：12、24、36、60个月的生存预测
- **生存曲线**：可视化展示生存概率随时间的变化
- **临床建议**：根据风险等级提供个性化建议

## 模型信息

- 模型类型：额外生存树
- 训练样本数：根据数据集
- C-index：模型评价指标

## 技术栈

- **后端**：Python + Streamlit
- **机器学习**：scikit-survival
- **数据处理**：pandas, numpy
- **可视化**：matplotlib

## 数据说明

- 数据文件：`data.csv`
- 特征：PSA, combine_metastasis, Age, T_stage, N_stage, Gleason
- 目标：event（事件），time（时间，单位：月）

## 注意事项

⚠️ 本系统仅供医学研究和教育参考，不可替代专业医疗诊断和治疗建议。
请在临床决策前咨询专业医师。

## 文件结构

```
.
├── app.py                      # Streamlit Web应用
├── train_model.py              # 模型训练脚本
├── data.csv                    # 训练数据
├── requirements.txt            # Python依赖
├── extra_survival_trees_model.pkl  # 训练好的模型（运行train_model.py后生成）
└── model_info.json             # 模型信息（运行train_model.py后生成）
```

## 问题排查

如果遇到依赖安装问题：

```bash
# 单独安装scikit-survival（可能需要先安装编译工具）
pip install scikit-survival
```

如果遇到显示问题：

```bash
# 清除Streamlit缓存
streamlit cache clear
```

## 作者

前列腺癌骨转移生存预测项目组

## 许可证

仅供科研使用
