## 1. なぜ `PdfMerger` が「非推奨」だと誤解されるのか

| 旧クラス | 新クラス | 非推奨（Deprecated） |
|----------|----------|------------------------|
| `PdfFileMerger` | `PdfMerger` | ✅ |
| `PdfFileReader`  | `PdfReader`  | ✅ |
| `PdfFileWriter`  | `PdfWriter`  | ✅ |

- **PyPDF2** から **pypdf** に移行したときに、旧クラス名（`PdfFileMerger` など）は非推奨化され、**`PdfMerger`** という新しい名前に置き換わりました。  
- **`PdfMerger` そのものは推奨されており、非推奨ではありません**。  
  → もし `PdfMerger` を使っていて「deprecated」と警告が出る場合は、古いバージョンの `pypdf`（`pypdf==2.x` など）を使っている可能性があります。最新版（`pypdf>=3.0.0`）にアップグレードしてください。

---

## 2. 最新版 `pypdf` で PDF を結合する基本コード

### 2‑1. 使い方の概要

```python
from pypdf import PdfMerger          # ← 推奨クラス

# 1. PdfMerger を作成
merger = PdfMerger()

# 2. 1つずつ PDF を追加
merger.append("first.pdf")
merger.append("second.pdf")

# 3. 出力
merger.write("merged.pdf")
merger.close()                       # ← close でリソースを解放
```

#### コンテキストマネージャを使う（おすすめ）

```python
from pypdf import PdfMerger

pdf_paths = ["a.pdf", "b.pdf", "c.pdf"]
output_path = "all_in_one.pdf"

with PdfMerger() as merger:
    for pdf in pdf_paths:
        merger.append(pdf)
    merger.write(output_path)
```

`with` ブロックを使うと `close()` を呼ぶ手間が省け、ファイルの破損リスクも減ります。

---

## 3. よくあるユースケース別サンプル

| シナリオ | コード例 |
|---------|---------|
| **複数 PDF を順番に結合** | 上記 2‑1 を参照 |
| **ページ範囲を指定して結合** | `merger.append("sample.pdf", pages=(0, 2))`  <br>→ 0〜2 ページ目（0 から始まる）を結合 |
| **同じ PDF を複数回挿入** | `merger.append("dup.pdf")` を 2 回呼び出す |
| **ファイルオブジェクト（バイナリ）から結合** | `with open(path, "rb") as f: merger.append(f)` |
| **特定のページだけ逆順で結合** | `merger.append(pdf_path, pages=[-1, -2, -3])` |

### 3‑1. ページ範囲を柔軟に扱う例

```python
def merge_with_page_range(pdf_paths, page_specs, output):
    """
    pdf_paths  : [str, ...]   例: ["a.pdf", "b.pdf"]
    page_specs : [tuple, ...] 例: [(0, 1), (0, None)]  # (start, end)  end=None は末尾まで
    """
    with PdfMerger() as merger:
        for path, spec in zip(pdf_paths, page_specs):
            start, end = spec
            merger.append(path, pages=(start, end))
        merger.write(output)
```

---

## 4. 旧バージョンで起きる典型的なエラーと対策

| エラー | 原因 | 解決策 |
|--------|------|--------|
| `DeprecationWarning: PdfFileMerger is deprecated` | `PdfFileMerger` を使っている | `PdfMerger` に置き換える |
| `ModuleNotFoundError: No module named 'PyPDF2'` | 古い `PyPDF2` を参照している | `pip install --upgrade pypdf` で最新版を入れる |
| `AttributeError: 'PdfMerger' object has no attribute 'append'` | 旧 API を呼び出している | `PdfMerger.append()` は正しいメソッド名です（`add()` ではない） |

**推奨**  
```bash
pip install --upgrade pypdf
```
（必要に応じて仮想環境を作ると安全です）

---

## 5. 参考にできる最小動作例（スクリプト全体）

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF を結合する最小スクリプト

使い方:
    python merge_pdfs.py output.pdf input1.pdf input2.pdf ...
"""

import sys
from pathlib import Path
from pypdf import PdfMerger

def main(argv):
    if len(argv) < 3:
        print("Usage: python merge_pdfs.py output.pdf input1.pdf input2.pdf ...")
        sys.exit(1)

    output_pdf = Path(argv[1])
    input_pdfs = [Path(p) for p in argv[2:]]

    # すべての入力が存在するかチェック
    for p in input_pdfs:
        if not p.is_file():
            print(f"Error: {p} does not exist.")
            sys.exit(1)

    with PdfMerger() as merger:
        for p in input_pdfs:
            merger.append(str(p))
        merger.write(str(output_pdf))

    print(f"Successfully created: {output_pdf}")

if __name__ == "__main__":
    main(sys.argv)
```

このスクリプトは：

1. コマンドライン引数で入力 PDF と出力ファイルを受け取る。  
2. `PdfMerger` を使って順番に PDF を追加。  
3. すべてのページを結合した結果を `output.pdf` に書き出す。  

---

## 6. まとめ

- **`PdfMerger` は推奨クラス**。古い `PdfFileMerger` が非推奨化。  
- **最新版 `pypdf`** をインストールして `PdfMerger` を利用すれば、警告は出ません。  
- **コンテキストマネージャ** (`with PdfMerger() as merger:`) を使うとリソース管理が楽。  
- ページ範囲やファイルオブジェクトを渡すことも容易。  

これで「非推奨」になっていると勘違いせず、確実に PDF を結合できるはずです。お試しください！
