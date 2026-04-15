---
name: lbc-awb-orders
description: 'Process LBC/BlindsByPost order files and DHL airway bills (AWBs). Matches order spreadsheets to AWB records by date, renames files with AWB prefixes, organizes into subfolders, and generates consolidated outputs for invoicing. Use when: processing new AWB shipment files; reconciling Zerolux or Tfpleated order files against DHL airway bills; splitting shipments by despatch month or surcharge band.'
argument-hint: 'AWBs.txt content or path, and BBP folder path'
user-invocable: true
---

# LBC AWB Order Processing

## When to Use

- A new set of DHL airway bills (AWBs) has arrived and needs to be matched to order files
- Order spreadsheets (Zerolux or Tfpleated) need renaming with AWB prefixes
- Consolidating shipment data for invoicing into Excel
- Splitting shipments by despatch month or surcharge percentage bands

---

## Step 1 — Gather Inputs

The agent needs two things:

1. **AWB data** — paste the full content of the AWBs.txt file directly into chat, **or** provide the file path if it already exists
2. **BBP folder path** — the path to the folder containing the Zerolux/Tfpleated order spreadsheets

> If the AWB data is provided via file path, confirm the path exists before proceeding.
> If pasting directly, the agent should save it to a working location and reference it from there.

---

## Step 2 — Initial Audit

Before making any changes:

1. List all files in the BBP folder
2. Parse the AWB text to extract:
   - AWB number (`AWB: 9355908170`)
   - Dispatch Date (`Dispatch Date: 27/03/2026`)
   - All carton/order lines (`---BlindsByPost-DD-MM-YYYY --- ...`)
3. Build a **date → AWB mapping** for both standard (`BlindsByPost-DD-MM-YYYY`) and FH (`BlindsByPost-FH-DD-MM-YYYY`) entries
4. Cross-reference: AWB dates ≤ today are valid; future dates are likely typos — flag these explicitly

**Key rules:**
- `tfpleated_` files only match `BlindsByPost-FH-` entries
- `zerolux_` files only match standard `BlindsByPost-DD-MM-YYYY` entries
- If the same date appears under multiple AWBs, use the **first** AWB only
- Future dates (beyond today) should be flagged as likely typos and excluded

---

## Step 3 — Reverse Check

Before renaming, verify that every carton/order line in the AWBs has a corresponding file in the BBP folder:
- For each date in each AWB, check if `zerolux_orders_YYYY-MM-DD.xlsx` or `tfpleated_orders_YYYY-MM-DD.xlsx` exists
- Report any missing files
- Report any files in BBP with no AWB match

---

## Step 4 — Dry Run

Always do a dry run first. Output a table showing:

| Original File Name | Matched Date | AWB Number | New File Name |
|---|---|---|---|

For files with no match, show `No match` in the AWB column.

Ask the user to confirm before proceeding.

---

## Step 5 — Rename and Organize

On user confirmation:

1. **Rename** each matched file in the BBP folder with AWB prefix: `AWBNUMBER_original_filename.xlsx`
2. **Create one subfolder per AWB number** (e.g. `9184073452/`)
3. **Move** the prefixed files into their corresponding AWB subfolder
4. **Create** a `_airwaybill.txt` file inside each AWB subfolder containing:
   - The original AWB block text (as provided in AWBs.txt)
   - All carton lines with box dimensions and weights
   - The DHL tracking URL

For AWBs provided manually (not in the original AWBs.txt file), create the `_airwaybill.txt` from the content the user pasted.

---

## Step 6 — Generate Master Files

After organizing:

1. **master_airwaybill.txt** — all carton lines from all AWB subfolders, tab-separated:
   - Column 1: AWB number
   - Column 2: Full carton line (e.g. `---BlindsByPost-21-03-2026 --- 191.5 x 18 x 18 (12.6kg) --- CHARGEABLE: 13kg`)
   - Save to BBP root

2. **Split by despatch month** (from `Dispatch Date:` in each AWB):
   - `master_airwaybill_MARCH.txt` — lines from AWBs despatched in March
   - `master_airwaybill_APRIL.txt` — lines from AWBs despatched in April
   - Always backup the original before splitting

---

## Step 7 — Zerolux Folder Prefix

If a separate **ZeroLux Orders** folder exists with copies of the same files:

1. List all files in that folder
2. Match them against the touched files from the BBP folder (by comparing original filename, e.g. `zerolux_orders_2026-03-17.xlsx`)
3. Prefix matched files with `invoiced_` (e.g. `invoiced_zerolux_orders_2026-03-17.xlsx`)
4. Do NOT move them — just rename in place

---

## Step 8 — Combined Excel Datasets

For the order spreadsheets inside each AWB subfolder:

1. Separate into two groups: `zerolux_` and `tfpleated_` (they have different column structures)
2. Combine all files in each group into a single tab-separated `.txt`:
   - **combined_zerolux.txt** — all Zerolux order rows
   - **combined_tfpleated.txt** — all Tfpleated order rows
   - Skip the header row in each spreadsheet
   - Convert all cells to strings, join with tabs
3. Save both to the BBP root

---

## Step 9 — Surcharge Bands (if applicable)

If surcharge percentages apply to the April/despatch period:

1. Ask user for the surcharge bands (date ranges and percentages)
2. For the April master file, look up the `Dispatch Date:` of each AWB to determine its surcharge %
3. Split the April file into separate files per band (e.g. `master_airwaybill_APRIL_39pct.txt`, `master_airwaybill_APRIL_46pct.txt`)
4. March file is typically left as-is at 30.50%

---

## Common Flags

| Flag | Action |
|------|--------|
| Future date in AWB (e.g. June 2026) | Likely typo — flag, exclude from matching, ask user to confirm correct date |
| Same date under multiple AWBs | Use first AWB only |
| tfpleated file but no FH entry in AWB | Flag as unmatched |
| .DS_Store files | Ignore — do not process |
| AWB with no matching files | Still create subfolder and _airwaybill.txt |

---

## Output Summary

At the end of processing, report:
- Number of files renamed and organized into subfolders
- Number of unmatched files (left in root or flagged)
- List of all generated files and their row/line counts
