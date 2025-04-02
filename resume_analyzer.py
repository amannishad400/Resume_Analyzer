import PyPDF2
import string


STOPWORDS = set([
    "a", "an", "the", "in", "on", "at", "for", "to", "and", "but", "or", 
    "of", "with", "by", "as", "from", "that", "which", "this", "is", "i","we" 
    "are", "was", "were", "be", "being", "been", "have", "has", "had","like"
])

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:  
                    text += page_text + "\n"
        return text.strip() 
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""


def get_resume_text(resume_text=None, pdf_path=None):
    if resume_text:
        return resume_text.strip() 
    elif pdf_path:
        extracted_text = extract_text_from_pdf(pdf_path)
        if not extracted_text:
            print("No text could be extracted from the PDF.")
        return extracted_text
    else:
        print("Error: No resume text or PDF path provided.")
        return ""

def match_keywords(resume_text, job_desc_text):
    
    resume_text= "".join([char for char in resume_text.lower() if char not in string.punctuation])
    job_desc_text = "".join([char for char in job_desc_text.lower() if char not in string.punctuation])

    resume_words = set(resume_text.split())
    job_desc_words = set(job_desc_text.split())

   
    resume_words = resume_words - STOPWORDS
    job_desc_words = job_desc_words - STOPWORDS
    

    common_words = resume_words.intersection(job_desc_words)
    
    return common_words


def calculate_similarity(resume_text, job_desc_text):
    common_words = match_keywords(resume_text, job_desc_text)

    resume_words = resume_text.split()
    job_desc_words = job_desc_text.split()

    total_words = len(job_desc_words)
    common_word_percentage = (len(common_words) / total_words) * 100 if total_words else 0

    return common_word_percentage, common_words


def analyze_resume(resume_text, job_desc_text):
    similarity_score, common_words = calculate_similarity(resume_text, job_desc_text)
    feedback = []

    if similarity_score > 70:
        feedback.append("Your resume is a great match for this job description!")
    elif similarity_score > 40:
        feedback.append("Your resume is a decent match for this job description.")
    else:
        feedback.append("Your resume could be improved to better match the job description.")

    feedback.append(f"Similarity Score: {similarity_score:.2f}%")
    feedback.append(f"Matched Keywords: {', '.join(common_words)}")
    
    return feedback

def main():
    n=input("\ndo you want to add manually a new job description, type (yes/NO)\n")
    if "yes" == n.lower().strip():
        job_desc_text = input('Enter job description:\n')
    elif "no" == n.lower().strip():
        job_desc_text = "web developer , python expert, html css"
    else:
        print("Invalid input")
        return

    pdf_path = input("Enter PDF path:\n").strip()
    resume_text_from_input = get_resume_text(pdf_path=pdf_path)
    if not resume_text_from_input:
        print("Error: No text was extracted from the resume.")
        return

    feedback = analyze_resume(resume_text_from_input, job_desc_text)

    print("\nAnalysis Results:")
    for line in feedback:
        print(line)

main()
