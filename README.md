# Analytical Lexicon and Concordance of the Greek New Testament  
## with eBible.gr Reference Links

This repository contains a Python script that adds **interactive Bible reference hyperlinks** to a PDF file of the work  
**Analytical Lexicon and Concordance of the Greek New Testament**.

The script detects biblical references such as *Mt 7:3*, *Lk 6:14*, *Jn 1:19–23*, etc., within the text and converts them into clickable links pointing to **ebible.gr**, allowing direct navigation from lexicon entries to the biblical text.

---

## 📖 About the Source Work

This project is designed to work with the following scholarly publication:

> **Analytical Lexicon and Concordance of the Greek New Testament**  
> Copyright © 2025 by **Alan Bunning**. All rights reserved.  
> **Center for New Testament Restoration**  
> *January 28, 2025 electronic edition*

This work is released under the  
**Creative Commons Attribution–ShareAlike 4.0 International License (CC BY-SA 4.0)**.

Attribution **must** be given to **Alan Bunning** and the **Center for New Testament Restoration** in any derivative works, and any changes made must be clearly indicated.

A printed version of this work has been published by **GlossaHouse**  
https://glossahouse.com  
and is priced to recover the publisher’s costs, with **no profit** going to Alan Bunning or the Center for New Testament Restoration.

---

## Textual Criticism and Collation of Greek Manuscripts

The links to **ebible.gr** provide access to a **manuscript collation** view in which Greek New Testament witnesses are compared verse by verse, revealing **textual variants** between early manuscripts and modern critical texts.  

In addition, the interface includes **three modern Greek translations**, facilitating more accessible engagement with the ancient Greek text.

Below is an example of the **manuscript collation interface** on **ebible.gr**, where Greek New Testament witnesses are compared verse by verse, highlighting **textual variants** and supported by interlinear analysis and modern Greek translations.

<img width="1098" height="789" alt="{7D0FBC67-2E52-4148-917A-520A768CA24F}" src="https://github.com/user-attachments/assets/09cfd1f9-3163-4bb9-944a-74259d5d3544" />

---

## ✨ Features

- PDF processing using **PyMuPDF (fitz)**
- Detection of biblical references:
  - Full references: `Mt 7:3–5`
  - Chapter–verse references: `Lk 6:14`
  - Verse-only references with inherited context
- Support for **superscript footnote markers** (e.g. `6:14³⁵`)
- Correct context inheritance across **line breaks and page breaks**
- Automatic generation of links such as:
  ```
  https://ebible.gr/collate/luk.6.14
  ```
- The original PDF content is preserved (only hyperlinks are added)

---

## 📁 Files

- `add_links.py`  
  The main Python script that scans the PDF and inserts hyperlinks.

- `ALC.pdf`  
  The original PDF file (not included in this repository due to copyright).

- `ALC_ebible_links.pdf`  
  The generated PDF with active Bible reference links.

---

## ⚙️ Requirements

- Python **3.9+**
- PyMuPDF

Install the dependency:

```bash
pip install pymupdf
```

---

## ▶️ Usage

1. Place the source PDF in the same directory as the script:
   ```text
   ALC.pdf
   ```

2. Run the script:
   ```bash
   python add_links.py
   ```

3. The output file will be created:
   ```text
   ALC_ebible_links.pdf
   ```

with clickable Bible references throughout the document.

---

## 🧠 Technical Notes

- The script reads the PDF at **character level** using `rawdict`
- Superscript footnote digits are ignored so that:
  - `Lk 6:14³⁵` → `luk 6:14`
- A combination of **regular expressions and contextual inheritance**
  ensures accurate interpretation of verse-only references
- Hyperlinks are inserted using precise bounding boxes around the detected text

---

## Web Conversion

The work **Analytical Lexicon and Concordance of the Greek New Testament** has also been converted into an **interactive web edition**, available at:

👉 **https://www.ebible.gr/alc**

The web version provides:
- direct navigation through lexicographical entries,
- active Bible reference links,
- access to **textual criticism** and **manuscript collation** tools,
- comparison of Greek manuscript witnesses and critical texts,
- parallel display of modern Greek translations,
- and a built-in **search functionality** for lexicon entries.

In addition, the web edition supports **URL-based search queries**, allowing direct access to search results using the following syntax:
   ```text
   https://www.ebible.gr/alc?q={word}
   ```
Search queries are processed **without diacritics (accents)**, enabling flexible and user-friendly lookup of Greek words regardless of accentuation.


