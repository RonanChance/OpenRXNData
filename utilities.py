import json

def clean_text(text):
    return ''.join(char for char in text if 32 <= ord(char) <= 126)

def gpt_prep():
    with open('mydatav2.json', 'r', encoding="utf-8") as json_file:
        data = json.load(json_file)

    for idx, dictionary in enumerate(data):
        if idx < 1000:
            filenum = 1
        elif idx < 2000:
            filenum = 2
        elif idx < 3000:
            filenum = 3
        elif idx < 4000:
            filenum = 4
        elif idx < 5000:
            filenum = 5
        elif idx < 6000:
            filenum = 6
        
        with open("./files/" + str(filenum) + ".csv", "a", encoding='utf-8') as chatgpt_file:
            try: 
                chatgpt_file.write(clean_text(dictionary['body']) + "\n")
                print(clean_text(dictionary['body']))
            except Exception:
                print("FOUND ISSUE")
                exit()
                continue
        
def wikipedia_link_generation():
    illnesses = ['ANAPLASMOSIS', 'BABESIOSIS', 'BARTONELLOSIS', 'EHRLICHIOSIS', 'LYME DISEASE', 'ROCKY MOUNTAIN SPOTTED FEVER', 'TULAREMIA']
    medications = ['ACETAMINOPHEN', 'ACETAZOLAMIDE', 'ACYCLOVIR', 'ALPRAZOLAM', 'AMITRIPTYLINE', 'AMOXICILLIN', 'ARIPIPRAZOLE', 'AZITHROMYCIN', 'AZLOCILLIN', 'BOTULINUM TOXIN TYPE A', 'CEFTRIAXONE', 'CEFUROXIME', 'CELECOXIB', 'CEPHALEXIN', 'CETIRIZINE', 'CHOLESTYRAMINE', 'CIPROFLOXACIN', 'CITALOPRAM', 'CLARITHROMYCIN', 'CLINDAMYCIN', 'CLONAZEPAM', 'COLCHICINE', 'CROMOGLICIC ACID', 'CYCLOBENZAPRINE', 'DAPTOMYCIN', 'DEXAMETHASONE', 'DIAZEPAM', 'DICYCLOMINE', 'DIPHENHYDRAMINE', 'DISULFIRAM', 'DOXYCYCLINE', 'DULOXETINE', 'ESCITALOPRAM', 'ESOMEPRAZOLE', 'FENTANYL', 'FLUCONAZOLE', 'FLUOXETINE', 'FLUVOXAMINE', 'HYDROCODONE', 'HYDROCORTISONE', 'HYDROXYCHLOROQUINE', 'HYDROXYZINE', 'L-TRYPTOPHAN', 'LEVOFLOXACIN', 'LEVOTHYROXINE', 'LIOTHYRONINE', 'LORAZEPAM', 'MECLIZINE', 'MELOXICAM', 'METHOTREXATE', 'METHYLPHENIDATE', 'METHYLPREDNISOLONE', 'METRONIDAZOLE', 'MINOCYCLINE', 'MIRTAZAPINE', 'NALTREXONE', 'NAPROXEN', 'NIACIN', 'NORTRIPTYLINE', 'NYSTATIN', 'OMEPRAZOLE', 'ONDANSETRON', 'OXYCODONE', 'PANTOPRAZOLE', 'PAROXETINE', 'PENICILLIN G', 'PREGABALIN', 'PROMETHAZINE', 'RANITIDINE', 'RIFAMPIN', 'RIFAXIMIN', 'SERTRALINE', 'TETRACYCLINE', 'TINIDAZOLE', 'TOPIRAMATE', 'TRAZODONE', 'VALACICLOVIR', 'VANCOMYCIN', 'VENLAFAXINE', 'ZINC']

    medication_dict = {}

    for item in medications:
        medication_dict[item] = "https://en.wikipedia.org/wiki/" + item.replace(" ", "_").lower()

    print(medication_dict)
    print(len(medications))