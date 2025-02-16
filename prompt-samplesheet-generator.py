import os
import re
import csv
from glob import glob
from collections import defaultdict

# Pipeline configurations
PIPELINE_CONFIG = {
    "sarek": {
        "columns": ["patient", "sex", "status", "sample", "lane", "fastq_1", "fastq_2"],
        "defaults": {"sex": "XX", "lane": "lane_1"},
        "filename": "samplesheet.csv",
        "description": "Sarek pipeline for variant calling (WES/WGS)"
    },
    "oncoanalyser": {
        "columns": ["group_id", "subject_id", "sample_id", "sample_type", "sequence_type", "filetype", "info", "filepath"],
        "defaults": {"filetype": "fastq"},
        "filename": "onco_samplesheet.csv",
        "description": "Oncoanalyser pipeline for cancer analysis (DNA/RNA)"
    },
    "rnaseq": {
        "columns": ["sample", "fastq_1", "fastq_2", "strandedness"],
        "defaults": {"strandedness": "auto"},
        "filename": "rnaseq_samplesheet.csv",
        "description": "RNAseq pipeline for transcriptome analysis"
    },
    "viralcon": {
        "columns": ["sample", "fastq_1", "fastq_2"],
        "defaults": {},
        "filename": "viral_samplesheet.csv",
        "description": "Viralcon pipeline for viral genome analysis"
    }
}

def get_pipeline_choice():
    """Prompt user to select a pipeline"""
    print("Available pipelines:")
    for i, (name, config) in enumerate(PIPELINE_CONFIG.items(), 1):
        print(f"{i}. {name} - {config['description']}")
    
    while True:
        choice = input("Enter pipeline number: ").strip()
        try:
            index = int(choice) - 1
            selected = list(PIPELINE_CONFIG.keys())[index]
            return selected
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.")

def get_input_directory():
    """Prompt user to input the directory containing FastQ files"""
    while True:
        input_dir = input("Enter the full path to the directory containing FastQ files: ").strip()
        if os.path.isdir(input_dir):
            return input_dir
        print(f"Error: Directory not found: {input_dir}. Please try again.")

def detect_samples(input_dir, pipeline):
    """Detect samples from FastQ files and extract metadata"""
    sample_dict = defaultdict(lambda: {"fastq_1": [], "fastq_2": []})
    
    # Match common FastQ patterns
    fastq_files = glob(os.path.join(input_dir, "*.f*q*.gz"))
    
    for file_path in sorted(fastq_files):
        filename = os.path.basename(file_path)
        
        if pipeline == "sarek":
            # Regex for Sarek filenames (e.g., 13-N_R1_001.fastq.gz)
            match = re.match(r"(\d+)(?:-([A-Za-z]+))?_?(R[12])_001\.f(?:ast)?q\.gz", filename)
            if match:
                patient_id = f"Patient_{match.group(1)}"
                status = "0" if match.group(2) == "N" else "1"  # 0 for Normal, 1 for Tumour
                sample_type = "Normal" if match.group(2) == "N" else "Tumour"
                read = match.group(3)
                
                # Create unique sample key
                sample_key = (patient_id, status, sample_type)
                
                if read == "R1":
                    sample_dict[sample_key]["fastq_1"].append(file_path)
                elif read == "R2":
                    sample_dict[sample_key]["fastq_2"].append(file_path)
            else:
                print(f"Skipping unrecognized file format: {filename}")
        
        elif pipeline == "viralcon":
            # Regex for Viralcon filenames (e.g., NG-A2794_TS219_libLAI2558_1.fastq.gz)
            match = re.match(r".+?_(.+?)_libLAI\d+_([12])\.f(?:ast)?q\.gz", filename)
            if match:
                sample_id = match.group(1)  # e.g., TS219
                read = match.group(2)  # 1 or 2
                
                # Create unique sample key
                sample_key = sample_id
                
                if read == "1":
                    sample_dict[sample_key]["fastq_1"].append(file_path)
                elif read == "2":
                    sample_dict[sample_key]["fastq_2"].append(file_path)
            else:
                print(f"Skipping unrecognized file format: {filename}")
        
        else:
            # Default regex for other pipelines
            match = re.match(r".+?_S\d+_L\d+_R([12])_001\.f(?:ast)?q\.gz", filename)
            if match:
                sample_id = filename.split("_")[0]  # Extract sample ID
                read = match.group(1)  # R1 or R2
                
                # Create unique sample key
                sample_key = sample_id
                
                if read == "1":
                    sample_dict[sample_key]["fastq_1"].append(file_path)
                elif read == "2":
                    sample_dict[sample_key]["fastq_2"].append(file_path)
            else:
                print(f"Skipping unrecognized file format: {filename}")
    
    return sample_dict

def generate_sarek_samplesheet(samples, output_dir):
    """Generate Sarek-compatible samplesheet"""
    csv_data = []
    
    for (patient, status, sample_type), reads in samples.items():
        # Ensure paired-end files exist
        if not reads["fastq_1"] or not reads["fastq_2"]:
            print(f"Skipping incomplete sample: {patient} ({sample_type})")
            continue
        
        # Add row to CSV data
        csv_data.append({
            "patient": patient,
            "sex": "XX",  # Default sex
            "status": status,
            "sample": sample_type,
            "lane": "lane_1",
            "fastq_1": ",".join(sorted(reads["fastq_1"])),
            "fastq_2": ",".join(sorted(reads["fastq_2"]))
        })
    
    # Write to CSV
    output_path = os.path.join(output_dir, PIPELINE_CONFIG["sarek"]["filename"])
    with open(output_path, "w") as f:
        writer = csv.DictWriter(f, fieldnames=PIPELINE_CONFIG["sarek"]["columns"], delimiter=",")
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"Successfully generated Sarek samplesheet at: {output_path}")

def generate_oncoanalyser_samplesheet(samples, output_dir):
    """Generate Oncoanalyser-compatible samplesheet"""
    csv_data = []
    
    for (sample_id, sequence_type, lane), reads in samples.items():
        # Ensure paired-end files exist
        if not reads["fastq_1"] or not reads["fastq_2"]:
            print(f"Skipping incomplete sample: {sample_id} ({sequence_type}, {lane})")
            continue
        
        # Extract subject ID and sample type
        subject_id = sample_id.split("_")[0]  # e.g., M171924D → M171924
        sample_type = "tumor"  # Default sample type
        
        # Prepare info field
        info = f"library_id:{sample_id}_library;lane:{lane}"
        
        # Add row to CSV data
        csv_data.append({
            "group_id": f"P{subject_id}_tso500",  # e.g., P1_tso500
            "subject_id": subject_id,
            "sample_id": sample_id,
            "sample_type": sample_type,
            "sequence_type": sequence_type,
            "filetype": "fastq",
            "info": info,
            "filepath": ";".join(sorted(reads["fastq_1"] + reads["fastq_2"]))
        })
    
    # Write to CSV
    output_path = os.path.join(output_dir, PIPELINE_CONFIG["oncoanalyser"]["filename"])
    with open(output_path, "w") as f:
        writer = csv.DictWriter(f, fieldnames=PIPELINE_CONFIG["oncoanalyser"]["columns"], delimiter=",")
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"Successfully generated Oncoanalyser samplesheet at: {output_path}")

def generate_rnaseq_samplesheet(samples, output_dir):
    """Generate RNAseq-compatible samplesheet"""
    csv_data = []
    
    for (sample_id, lane), reads in samples.items():
        # Ensure paired-end files exist
        if not reads["fastq_1"] or not reads["fastq_2"]:
            print(f"Skipping incomplete sample: {sample_id} (lane {lane})")
            continue
        
        # Add row to CSV data
        csv_data.append({
            "sample": sample_id,
            "fastq_1": ",".join(sorted(reads["fastq_1"])),
            "fastq_2": ",".join(sorted(reads["fastq_2"])),
            "strandedness": "auto"  # Default strandedness
        })
    
    # Write to CSV
    output_path = os.path.join(output_dir, PIPELINE_CONFIG["rnaseq"]["filename"])
    with open(output_path, "w") as f:
        writer = csv.DictWriter(f, fieldnames=PIPELINE_CONFIG["rnaseq"]["columns"], delimiter=",")
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"Successfully generated RNAseq samplesheet at: {output_path}")

def generate_viralcon_samplesheet(samples, output_dir):
    """Generate Viralcon-compatible samplesheet"""
    csv_data = []
    
    for sample_id, reads in samples.items():
        # Ensure paired-end files exist
        if not reads["fastq_1"] or not reads["fastq_2"]:
            print(f"Skipping incomplete sample: {sample_id}")
            continue
        
        # Add row to CSV data
        csv_data.append({
            "sample": sample_id,
            "fastq_1": ",".join(sorted(reads["fastq_1"])),
            "fastq_2": ",".join(sorted(reads["fastq_2"]))
        })
    
    # Write to CSV
    output_path = os.path.join(output_dir, PIPELINE_CONFIG["viralcon"]["filename"])
    with open(output_path, "w") as f:
        writer = csv.DictWriter(f, fieldnames=PIPELINE_CONFIG["viralcon"]["columns"], delimiter=",")
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"Successfully generated Viralcon samplesheet at: {output_path}")

def generate_samplesheet(pipeline, input_dir, output_dir="output"):
    """Generate samplesheet for the selected pipeline"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Detect samples from the input directory
    samples = detect_samples(input_dir, pipeline)
    
    # Generate the appropriate samplesheet
    if pipeline == "sarek":
        generate_sarek_samplesheet(samples, output_dir)
    elif pipeline == "oncoanalyser":
        generate_oncoanalyser_samplesheet(samples, output_dir)
    elif pipeline == "rnaseq":
        generate_rnaseq_samplesheet(samples, output_dir)
    elif pipeline == "viralcon":
        generate_viralcon_samplesheet(samples, output_dir)
    else:
        print(f"Pipeline '{pipeline}' is not yet implemented. Please provide the CSV format for this pipeline.")

if __name__ == "__main__":
    # Prompt user for pipeline choice
    selected_pipeline = get_pipeline_choice()
    
    # Prompt user for input directory
    input_dir = get_input_directory()
    
    # Generate samplesheet
    generate_samplesheet(selected_pipeline, input_dir)
