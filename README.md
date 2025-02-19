---

# 📁 nf-core Sample Sheet Generator 🧬

A Python script to generate sample sheets for various nf-core pipelines (e.g., Sarek, Oncoanalyser, RNAseq, Viralcon) from FastQ files. This tool automates the process of creating standardized sample sheets required for nf-core pipelines, saving time and reducing errors.

---

## 🚀 Features

- **Supports Multiple Pipelines** 🛠️  
  Generate sample sheets for:
  - **Sarek** (WES/WGS variant calling)
  - **Oncoanalyser** (cancer analysis)
  - **RNAseq** (transcriptome analysis)
  - **Viralcon** (viral genome analysis)

- **Non-Interactive** 🤖  
  Run the script directly from the command line with arguments for pipeline type and input directory.

- **FastQ File Detection** 🔍  
  Automatically detects FastQ files in the input directory and extracts metadata (e.g., sample names, read pairs).

- **Custom Output Directory** 📂  
  Specify an output directory for the generated sample sheets (default: `output`).

---

## 🛠️ Installation

1. **Clone the Repository**:
   ```bash
   git clone https://git.rz.uni-augsburg.de/obiorach/sample_sheet_generator.git

   cd nf-core-sample-sheet-generator
   ```

2. **Make the Script Executable**:
   ```bash
   chmod +x nfcore_sample_sheet_generator.py
   ```

3. **Run the Script**:
   ```bash
   ./nfcore_sample_sheet_generator.py -m <pipeline_mode> -i <input_directory> [-o <output_directory>]
   ```

---

## 🖥️ Usage

### Command-Line Arguments

| Argument       | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `-m`, `--mode` | Pipeline mode (`sarek`, `oncoanalyser`, `rnaseq`, `viralcon`).              |
| `-i`, `--input`| Path to the directory containing FastQ files.                               |
| `-o`, `--output`| (Optional) Output directory for the sample sheet (default: `output`).       |

### Examples

1. **Generate a Sample Sheet for Oncoanalyser**:
   ```bash
   ./nfcore_sample_sheet_generator.py -m oncoanalyser -i /path/to/fastq_files/
   ```

2. **Generate a Sample Sheet for Sarek with Custom Output Directory**:
   ```bash
   ./nfcore_sample_sheet_generator.py -m sarek -i /path/to/fastq_files/ -o sarek_output
   ```

3. **Generate a Sample Sheet for RNAseq**:
   ```bash
   ./nfcore_sample_sheet_generator.py -m rnaseq -i /path/to/fastq_files/
   ```

---

## 📂 Input Directory Structure

The script expects FastQ files in the input directory. The files should follow a naming convention compatible with the selected pipeline. For example:

- **Sarek**: `13-N_R1_001.fastq.gz`, `13-N_R2_001.fastq.gz`
- **Oncoanalyser**: `sample1_S1_L001_R1_001.fastq.gz`, `sample1_S1_L001_R2_001.fastq.gz`
- **RNAseq**: `sample1_R1.fastq.gz`, `sample1_R2.fastq.gz`
- **Viralcon**: `NG-A2794_TS219_libLAI2558_1.fastq.gz`, `NG-A2794_TS219_libLAI2558_2.fastq.gz`

---

## 📝 Output

The script generates a CSV file in the specified output directory. The file name and columns depend on the selected pipeline:

| Pipeline       | Output File Name       | Columns                                                                 |
|----------------|------------------------|-------------------------------------------------------------------------|
| **Sarek**      | `samplesheet.csv`      | `patient`, `sex`, `status`, `sample`, `lane`, `fastq_1`, `fastq_2`      |
| **Oncoanalyser**| `onco_samplesheet.csv`| `group_id`, `subject_id`, `sample_id`, `sample_type`, `sequence_type`, `filetype`, `info`, `filepath` |
| **RNAseq**     | `rnaseq_samplesheet.csv`| `sample`, `fastq_1`, `fastq_2`, `strandedness`                         |
| **Viralcon**   | `viral_samplesheet.csv`| `sample`, `fastq_1`, `fastq_2`                                         |

---

## 🐛 Troubleshooting

- **Unrecognized File Formats**:
  Ensure your FastQ files follow the expected naming convention for the selected pipeline.

- **Permission Denied**:
  Make the script executable using `chmod +x nfcore_sample_sheet_generator.py`.

- **Directory Not Found**:
  Double-check the input directory path and ensure it exists.

---

## 🤝 Contributing

Contributions are welcome! If you'd like to add support for more pipelines or improve the script, feel free to open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

---

## 📜 License

This project is licensed under the bioinformatics core facility Augsburg License. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by the nf-core community and their amazing pipelines.
- Thanks to Jan Meier-Kolthoff, for this insight into this project!

---

Made with ❤️ by Chukwuma Winner Obiora.  
Let's make bioinformatics easier, one script at a time! 🧬🚀

---

