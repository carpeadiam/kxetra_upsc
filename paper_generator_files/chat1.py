#this is a chat based file which gives a structured input 
#iisue is file upload is time intensive. 

import os
import time
import google.generativeai as genai
from flask import Blueprint

gemini = Blueprint('gemini', __name__)

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
question_count = 100

def upload_to_gemini(path, mime_type=None):
   file = genai.upload_file(path, mime_type=mime_type)
   print(f"Uploaded file '{file.display_name}' as: {file.uri}")
   return file

def wait_for_files_active(files):
 
  print("Waiting for file processing...")
  for name in (file.name for file in files):
    file = genai.get_file(name)
    while file.state.name == "PROCESSING":
      print(".", end="", flush=True)
      time.sleep(10)
      file = genai.get_file(name)
    if file.state.name != "ACTIVE":
      raise Exception(f"File {file.name} failed to process")
  print("...all files ready")
  print()

# Create the model
generation_config = {
  "temperature": 0.5,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

# TODO Make these files available on the local file system
# You may need to update the file paths
files = [ #currently only uploading exam 01 files
  upload_to_gemini("upsc papers/Pre_Exam_2023_Psper 1.pdf", mime_type="application/pdf"),
  upload_to_gemini("upsc papers/PAPER I 2022.pdf", mime_type="application/pdf"),
  upload_to_gemini("upsc papers/QP-CSP-24-GENERAL-STUDIES-PAPER-I-180624.pdf", mime_type="application/pdf"),
  upload_to_gemini("upsc papers/subjects in UPSC.pdf", mime_type="application/pdf"),
  # upload_to_gemini("upsc papers/PAPER II 2022.pdf", mime_type="application/pdf"),
  # upload_to_gemini("upsc papers/GENERAL_STUDIES_PAPER_II_2023.pdf", mime_type="application/pdf"),
  # upload_to_gemini("upsc papers/QP-CSP-24-GENERAL-STUDIES-PAPER-II-180624.pdf", mime_type="application/pdf"),
]

# Some files have a processing delay. Wait for them to be ready.
wait_for_files_active(files)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        files[0],
        files[1],
        files[2],
        "You are a paper setter for the UPSC examination. You are tasked to create practice papers for the UPSC prelims examination for your study platform of the same. You are supposed to include subjects such as economics, history and general knowledge among others. The difficulty is to be on par with the recent trends of the UPSC. \ngo through these 6 pdfs. They are the question papers of the past 3 years . Use them as reference while drafting the questions. the number of questions to be generated is 40.", 
      ],
    },
    {
      "role": "model",
      "parts": [
        "Here are 40 UPSC Prelims-style questions based on the provided PDFs, covering Economics, History, and General Knowledge.  The difficulty level aims to match recent UPSC trends.\n\n\n**Economics:**\n\n1.  What is the \"Real Effective Exchange Rate (REER)\" and how does its increase impact a nation's trade competitiveness?\n2.  Explain the concept of \"Inflation-Indexed Bonds (IIBs)\" and their advantages for governments and investors.\n3.  How do \"External Commercial Borrowings (ECBs)\" affect a country's currency risk, and what is the role of domestic currency devaluation in this context?\n4.  Describe the \"G20 Common Framework\" and its objective in addressing unsustainable debt in low-income countries.\n5.  What are the key differences between \"Nominal Effective Exchange Rate (NEER)\" and REER, and how do they reflect a nation's economic health?\n6.  Explain the concept of \"Indirect Transfers\" in the context of international taxation and its relevance to India.\n\n\n**History:**\n\n7.  What were the key provisions of the Government of India Act, 1935, regarding the establishment of the Indian Federation and the distribution of powers?\n8.  Identify the \"Reserved\" and \"Transferred\" subjects under the Government of India Act, 1919.\n9.  Describe the main features of the Cripps Mission proposals, and their impact on the future of India's constitutional development.\n10. Who were the key figures associated with the establishment of the English press in Colonial India?\n11. What were the major objectives of the Ayushman Bharat Digital Mission, and how does it aim to improve healthcare access and portability across India?\n12. Explain the concept of \"Scheduled Areas\" in India, and the role of the President and state governments in their administration.\n\n\n**General Knowledge:**\n\n13. What is the significance of the \"Stability and Growth Pact\" within the European Union?\n14. Explain the concept of \"Coriolis force\" and its impact on wind patterns.\n15. What is the \"Global Compact for Safe, Orderly and Regular Migration (GCM)\" and its key objectives?\n16. Explain the function of \"biofilters\" in recirculating aquaculture systems and their role in wastewater treatment.\n17. What is the \"Anaemia Mukt Bharat Strategy\" and its key components for addressing anaemia in India?\n18. What is the \"Janani Suraksha Yojana\" and its primary objectives in improving maternal and child health?\n19. What is the \"Pradhan Mantri Surakshit Matritva Abhiyan\" and its key provisions for providing antenatal and postnatal care to pregnant women?\n20. What is the \"Pradhan Mantri Shram Yogi Maan-dhan (PM-SYM)\" scheme, and what are its key features regarding pension provision for the unorganized sector?\n21. What is \"DNA barcoding\" and its applications in identifying species and detecting adulteration in food products?\n22. What is the \"Climate Action Tracker\" and its role in monitoring climate change mitigation pledges by different countries?\n23. What is \"greenwashing,\" and how does it manifest in corporate reporting and marketing practices?\n24. What are the key features of the \"Miyawaki method\" for urban afforestation?\n25. What is \"biomethanation\" and its role in managing municipal solid waste in India?\n26. What is the \"Digital India Land Records Modernisation Programme\" and its key objectives?\n27. What is the role of the \"Tea Board\" in India in regulating the tea industry?\n28. What is the significance of the \"Sumed Pipeline\" in transporting oil and gas from the Persian Gulf to Europe?\n29. What is the \"World Toilet Organization\" and its role in promoting global sanitation?\n30. What is the \"National Handloom Day\" and its significance in promoting India's handloom sector?\n31. What is the \"Fractional Orbital Bombardment System\" and its concept?\n32. What is the \"Nari Shakti Vandan Adhiniyam\" and its key provisions for women's empowerment?\n33. What is the \"Mitra Shakti-2023\" exercise and its key objectives?\n34. What is the \"India Sanitation Coalition\" and its role in promoting sustainable sanitation?\n35. What is the \"National Institute of Urban Affairs\" and its role in addressing urban challenges in India?\n36. What is the \"Net-Zero Industry Act\" recently approved by the European Parliament and its implications?\n\n\nThese questions are designed to test a wide range of knowledge and analytical skills, reflecting the diverse nature of the UPSC Prelims exam.  Remember to consult official UPSC resources and materials for the most accurate and up-to-date information.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "they are supposed to be multiple choice \n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Here are 40 multiple-choice questions for UPSC Prelims practice, based on the provided PDFs, covering Economics, History, and General Knowledge. The difficulty level aims to match recent UPSC trends.  Each question includes four options (a), (b), (c), and (d), with only one correct answer.\n\n\n**Economics:**\n\n1.  The Real Effective Exchange Rate (REER) is primarily a measure of:\n    (a) Nominal exchange rate fluctuations.\n    (b) A country's trade competitiveness.\n    (c) Domestic inflation relative to other countries.\n    (d) Capital flows into and out of a country.\n\n2.  Inflation-Indexed Bonds (IIBs) offer which key advantage to investors?\n    (a) Guaranteed high returns regardless of inflation.\n    (b) Protection against inflation uncertainty.\n    (c) Tax exemption on all interest and capital gains.\n    (d) Direct access to government spending programs.\n\n3.  External Commercial Borrowings (ECBs) in India are most significantly affected by:\n    (a) Domestic interest rate changes.\n    (b) Global commodity price fluctuations.\n    (c) Domestic currency devaluation.\n    (d) Changes in the US Federal Reserve's monetary policy.\n\n4.  The G20 Common Framework primarily aims to:\n    (a) Provide debt relief to all low-income countries.\n    (b) Promote sustainable development in emerging economies.\n    (c) Support low-income countries with unsustainable debt.\n    (d) Encourage foreign direct investment in developing nations.\n\n5.  The difference between Nominal Effective Exchange Rate (NEER) and REER lies primarily in:\n    (a) The currency used for calculation.\n    (b) The inclusion of trade volumes in REER.\n    (c) The consideration of inflation in REER.\n    (d) The time period considered for calculation.\n\n6.  \"Indirect Transfers\" in international taxation primarily refer to:\n    (a) Transfer of physical assets between countries.\n    (b) Transfer of profits from assets located in one country to another.\n    (c) Transfer of funds through international banking systems.\n    (d) Transfer of intellectual property rights between countries.\n\n\n**History:**\n\n7.  The Government of India Act, 1935, established:\n    (a) A completely unitary system of governance.\n    (b) A federal structure with significant provincial autonomy.\n    (c) A quasi-federal system with limited provincial powers.\n    (d) A fully independent system of governance for India.\n\n8.  Under the Government of India Act, 1919, which were considered \"Reserved Subjects\"?\n    (a) Education, health, and local self-government.\n    (b) Law and order, land revenue, and irrigation.\n    (c) Justice, police, and local self-government.\n    (d)  Irrigation, public health, and education.\n\n9.  The Cripps Mission's proposals primarily focused on:\n    (a) Immediate independence for India.\n    (b) Dominion status for India after the war.\n    (c) A plan for a post-war constituent assembly.\n    (d)  A framework for a future Indian federation.\n\n10. Which figure is NOT prominently associated with the early establishment of the English press in India?\n     (a) Raja Rammohun Roy\n     (b) Alexander Rea\n     (c) James Augustus Hickey\n     (d) Walter Elliot\n\n11. A key objective of the Ayushman Bharat Digital Mission is to:\n     (a) Provide free healthcare to all citizens.\n     (b) Improve the quality of healthcare infrastructure.\n     (c) Ensure seamless portability of health records.\n     (d) Eliminate private healthcare providers from the system.\n\n12. In India, \"Scheduled Areas\" are primarily defined and administered by:\n     (a) The Parliament.\n     (b) The President and State Governments.\n     (c) The Union Ministry of Home Affairs.\n     (d) The Supreme Court of India.\n\n\n**General Knowledge:**\n\n13. The European Union's \"Stability and Growth Pact\" primarily aims to:\n     (a) Promote economic growth within the EU.\n     (b) Limit the levels of budgetary deficits in EU member states.\n     (c) Facilitate free movement of people within the EU.\n     (d) Standardize environmental regulations across the EU.\n\n14. The Coriolis effect is most pronounced at:\n     (a) The equator.\n     (b) The tropics.\n     (c) Mid-latitudes.\n     (d) The poles.\n\n15. The \"Global Compact for Safe, Orderly and Regular Migration\" primarily aims to:\n     (a) Eliminate illegal migration worldwide.\n     (b) Promote international cooperation on migration issues.\n     (c) Restrict migration from developing countries.\n     (d) Prioritize the needs of migrant workers.\n\n16. Biofilters in recirculating aquaculture systems primarily function to:\n     (a) Increase fish growth rates.\n     (b) Convert ammonia waste into nitrates.\n     (c) Enhance oxygen levels in the water.\n     (d) Remove uneaten fish feed from the water.\n\n17. The Anaemia Mukt Bharat Strategy focuses primarily on:\n     (a) Providing iron supplements to all citizens.\n     (b) Addressing nutritional deficiencies in children and women.\n     (c) Improving sanitation and hygiene practices.\n     (d) Increasing access to healthcare services.\n\n18. The Janani Suraksha Yojana's main objective is to:\n     (a) Provide financial assistance to all pregnant women.\n     (b) Reduce maternal and infant mortality rates.\n     (c) Promote institutional deliveries among all women.\n     (d) Improve the quality of healthcare facilities in rural areas.\n\n19. The Pradhan Mantri Surakshit Matritva Abhiyan primarily guarantees:\n     (a) Free antenatal and postnatal care for all pregnant women.\n     (b) Minimum package of antenatal and postnatal care for pregnant women in government facilities.\n     (c) Financial assistance for all deliveries in private hospitals.\n     (d) Access to family planning services for all women.\n\n20. The Pradhan Mantri Shram Yogi Maan-dhan (PM-SYM) Yojana primarily aims to:\n     (a) Provide social security benefits to all citizens.\n     (b) Provide old-age pensions to workers in the unorganized sector.\n     (c) Provide healthcare benefits to workers in the unorganized sector.\n     (d) Provide unemployment benefits to workers in the unorganized sector.\n\n21. DNA barcoding can be used to:\n     (a) Determine the age of a plant or animal.\n     (b) Identify genetically modified organisms.\n     (c) Distinguish between similar-looking species.\n     (d) Detect the presence of harmful substances in food.\n\n22. The \"Climate Action Tracker\" is primarily a:\n     (a) UN agency monitoring climate change.\n     (b) Database tracking national climate pledges.\n     (c) Scientific model predicting future climate scenarios.\n     (d) International organization promoting climate action.\n\n23. \"Greenwashing\" in the context of corporate social responsibility refers to:\n     (a) Companies' actual environmental performance.\n     (b) Companies' misleading claims about their environmental impact.\n     (c) Government regulations on environmental reporting.\n     (d) International standards for environmental sustainability.\n\n24. The Miyawaki method is primarily associated with:\n     (a) Large-scale reforestation projects.\n     (b) Urban afforestation and creating mini-forests.\n     (c) Sustainable agriculture practices.\n     (d) Soil conservation techniques.\n\n25. Biomethanation is most relevant to which sector in India?\n     (a) Agriculture\n     (b) Municipal waste management\n     (c) Industrial wastewater treatment\n     (d) Energy generation\n\n26. The Digital India Land Records Modernisation Programme's main goal is:\n     (a) To digitize all land records in India.\n     (b) To improve land administration in rural areas.\n     (c) To provide land ownership certificates to all citizens.\n     (d) To promote transparency in land transactions.\n\n27. The Tea Board in India primarily functions to:\n     (a) Promote tea consumption in India.\n     (b) Regulate the tea industry in India.\n     (c) Export Indian tea to international markets.\n     (d) Provide financial assistance to tea farmers.\n\n28. The Sumed Pipeline is significant for:\n     (a) Transporting oil and gas from the Persian Gulf to Europe.\n     (b) Connecting the Red Sea and the Mediterranean Sea.\n     (c) Providing water to arid regions in the Middle East.\n     (d) Transporting natural gas from Russia to Europe.\n\n29. The World Toilet Organization's primary focus is on:\n     (a) Providing toilets in urban areas.\n     (b) Promoting global sanitation initiatives.\n     (c) Funding sanitation projects in developing countries.\n     (d) Manufacturing and distributing toilets worldwide.\n\n30. National Handloom Day in India is celebrated to:\n     (a) Commemorate the invention of the handloom.\n     (b) Promote the use of handloom products.\n     (c) Recognize the contribution of handloom weavers.\n     (d) Protect traditional handloom techniques from extinction.\n\n31. The Fractional Orbital Bombardment System (FOBS) is primarily associated with:\n     (a) Space-based missile defense systems.\n     (b) Hypersonic missile technology.\n     (c) Low Earth orbit satellite deployment.\n     (d) Anti-satellite weapon systems.\n\n32. The Nari Shakti Vandan Adhiniyam primarily focuses on:\n     (a) Women's political representation.\n     (b) Women's economic empowerment.\n     (c) Women's health and safety.\n     (d) Reservation for women in government jobs.\n\n33. The Mitra Shakti-2023 military exercise involved:\n     (a) India and China.\n     (b) India and Pakistan.\n     (c) India and Bangladesh.\n     (d) India and Sri Lanka.\n\n34. The India Sanitation Coalition is primarily:\n     (a) A government agency.\n     (b) A UN-backed organization.\n     (c) A non-profit organization promoting sustainable sanitation.\n     (d) An international consortium of sanitation companies.\n\n35. The National Institute of Urban Affairs primarily focuses on:\n     (a) Urban planning and development.\n     (b) Urban infrastructure development.\n     (c) Urban poverty alleviation.\n     (d) Addressing urban governance challenges.\n\n36. The Net-Zero Industry Act, recently passed by the European Parliament, aims to:\n     (a) Reduce carbon emissions from all industries.\n     (b) Promote the use of renewable energy sources.\n     (c) Achieve carbon neutrality by 2040 in the EU.\n     (d) Invest in clean technology development within the EU.\n\n\nThese questions are designed to test a wide range of knowledge and analytical skills, reflecting the diverse nature of the UPSC Prelims exam.  Remember to consult official UPSC resources and materials for the most accurate and up-to-date information.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "can u give the same in a json form minus the explaination at the end?\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\n  \"questions\": [\n    {\n      \"question\": \"The Real Effective Exchange Rate (REER) is primarily a measure of:\",\n      \"options\": {\n        \"a\": \"Nominal exchange rate fluctuations.\",\n        \"b\": \"A country's trade competitiveness.\",\n        \"c\": \"Domestic inflation relative to other countries.\",\n        \"d\": \"Capital flows into and out of a country.\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"Inflation-Indexed Bonds (IIBs) offer which key advantage to investors?\",\n      \"options\": {\n        \"a\": \"Guaranteed high returns regardless of inflation.\",\n        \"b\": \"Protection against inflation uncertainty.\",\n        \"c\": \"Tax exemption on all interest and capital gains.\",\n        \"d\": \"Direct access to government spending programs.\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"External Commercial Borrowings (ECBs) in India are most significantly affected by:\",\n      \"options\": {\n        \"a\": \"Domestic interest rate changes.\",\n        \"b\": \"Global commodity price fluctuations.\",\n        \"c\": \"Domestic currency devaluation.\",\n        \"d\": \"Changes in the US Federal Reserve's monetary policy.\"\n      },\n      \"answer\": \"c\"\n    },\n    {\n      \"question\": \"The G20 Common Framework primarily aims to:\",\n      \"options\": {\n        \"a\": \"Provide debt relief to all low-income countries.\",\n        \"b\": \"Promote sustainable development in emerging economies.\",\n        \"c\": \"Support low-income countries with unsustainable debt.\",\n        \"d\": \"Encourage foreign direct investment in developing nations.\"\n      },\n      \"answer\": \"c\"\n    },\n    {\n      \"question\": \"The difference between Nominal Effective Exchange Rate (NEER) and REER lies primarily in:\",\n      \"options\": {\n        \"a\": \"The currency used for calculation.\",\n        \"b\": \"The inclusion of trade volumes in REER.\",\n        \"c\": \"The consideration of inflation in REER.\",\n        \"d\": \"The time period considered for calculation.\"\n      },\n      \"answer\": \"c\"\n    },\n    {\n      \"question\": \"\\\"Indirect Transfers\\\" in international taxation primarily refer to:\",\n      \"options\": {\n        \"a\": \"Transfer of physical assets between countries.\",\n        \"b\": \"Transfer of profits from assets located in one country to another.\",\n        \"c\": \"Transfer of funds through international banking systems.\",\n        \"d\": \"Transfer of intellectual property rights between countries.\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"The Government of India Act, 1935, established:\",\n      \"options\": {\n        \"a\": \"A completely unitary system of governance.\",\n        \"b\": \"A federal structure with significant provincial autonomy.\",\n        \"c\": \"A quasi-federal system with limited provincial powers.\",\n        \"d\": \"A fully independent system of governance for India.\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"Under the Government of India Act, 1919, which were considered \\\"Reserved Subjects\\\"?\",\n      \"options\": {\n        \"a\": \"Education, health, and local self-government.\",\n        \"b\": \"Law and order, land revenue, and irrigation.\",\n        \"c\": \"Justice, police, and local self-government.\",\n        \"d\": \"Irrigation, public health, and education.\"\n      },\n      \"answer\": \"c\"\n    },\n    {\n      \"question\": \"The Cripps Mission's proposals primarily focused on:\",\n      \"options\": {\n        \"a\": \"Immediate independence for India.\",\n        \"b\": \"Dominion status for India after the war.\",\n        \"c\": \"A plan for a post-war constituent assembly.\",\n        \"d\": \"A framework for a future Indian federation.\"\n      },\n      \"answer\": \"c\"\n    },\n    {\n      \"question\": \"Which figure is NOT prominently associated with the early establishment of the English press in India?\",\n      \"options\": {\n        \"a\": \"Raja Rammohun Roy\",\n        \"b\": \"Alexander Rea\",\n        \"c\": \"James Augustus Hickey\",\n        \"d\": \"Walter Elliot\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"A key objective of the Ayushman Bharat Digital Mission is to:\",\n      \"options\": {\n        \"a\": \"Provide free healthcare to all citizens.\",\n        \"b\": \"Improve the quality of healthcare infrastructure.\",\n        \"c\": \"Ensure seamless portability of health records.\",\n        \"d\": \"Eliminate private healthcare providers from the system.\"\n      },\n      \"answer\": \"c\"\n    },\n    {\n      \"question\": \"In India, \\\"Scheduled Areas\\\" are primarily defined and administered by:\",\n      \"options\": {\n        \"a\": \"The Parliament.\",\n        \"b\": \"The President and State Governments.\",\n        \"c\": \"The Union Ministry of Home Affairs.\",\n        \"d\": \"The Supreme Court of India.\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"The European Union's \\\"Stability and Growth Pact\\\" primarily aims to:\",\n      \"options\": {\n        \"a\": \"Promote economic growth within the EU.\",\n        \"b\": \"Limit the levels of budgetary deficits in EU member states.\",\n        \"c\": \"Facilitate free movement of people within the EU.\",\n        \"d\": \"Standardize environmental regulations across the EU.\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"The Coriolis effect is most pronounced at:\",\n      \"options\": {\n        \"a\": \"The equator.\",\n        \"b\": \"The tropics.\",\n        \"c\": \"Mid-latitudes.\",\n        \"d\": \"The poles.\"\n      },\n      \"answer\": \"d\"\n    },\n    {\n      \"question\": \"The \\\"Global Compact for Safe, Orderly and Regular Migration\\\" primarily aims to:\",\n      \"options\": {\n        \"a\": \"Eliminate illegal migration worldwide.\",\n        \"b\": \"Promote international cooperation on migration issues.\",\n        \"c\": \"Restrict migration from developing countries.\",\n        \"d\": \"Prioritize the needs of migrant workers.\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"Biofilters in recirculating aquaculture systems primarily function to:\",\n      \"options\": {\n        \"a\": \"Increase fish growth rates.\",\n        \"b\": \"Convert ammonia waste into nitrates.\",\n        \"c\": \"Enhance oxygen levels in the water.\",\n        \"d\": \"Remove uneaten fish feed from the water.\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"The Anaemia Mukt Bharat Strategy focuses primarily on:\",\n      \"options\": {\n        \"a\": \"Providing iron supplements to all citizens.\",\n        \"b\": \"Addressing nutritional deficiencies in children and women.\",\n        \"c\": \"Improving sanitation and hygiene practices.\",\n        \"d\": \"Increasing access to healthcare services.\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"The Janani Suraksha Yojana's main objective is to:\",\n      \"options\": {\n        \"a\": \"Provide financial assistance to all pregnant women.\",\n        \"b\": \"Reduce maternal and infant mortality rates.\",\n        \"c\": \"Promote institutional deliveries among all women.\",\n        \"d\": \"Improve the quality of healthcare facilities in rural areas.\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"The Pradhan Mantri Surakshit Matritva Abhiyan primarily guarantees:\",\n      \"options\": {\n        \"a\": \"Free antenatal and postnatal care for all pregnant women.\",\n        \"b\": \"Minimum package of antenatal and postnatal care for pregnant women in government facilities.\",\n        \"c\": \"Financial assistance for all deliveries in private hospitals.\",\n        \"d\": \"Access to family planning services for all women.\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"The Pradhan Mantri Shram Yogi Maan-dhan (PM-SYM) Yojana primarily aims to:\",\n      \"options\": {\n        \"a\": \"Provide social security benefits to all citizens.\",\n        \"b\": \"Provide old-age pensions to workers in the unorganized sector.\",\n        \"c\": \"Provide healthcare benefits to workers in the unorganized sector.\",\n        \"d\": \"Provide unemployment benefits to workers in the unorganized sector.\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"DNA barcoding can be used to:\",\n      \"options\": {\n        \"a\": \"Determine the age of a plant or animal.\",\n        \"b\": \"Identify genetically modified organisms.\",\n        \"c\": \"Distinguish between similar-looking species.\",\n        \"d\": \"Detect the presence of harmful substances in food.\"\n      },\n      \"answer\": \"c\"\n    },\n    {\n      \"question\": \"The \\\"Climate Action Tracker\\\" is primarily a:\",\n      \"options\": {\n        \"a\": \"UN agency monitoring climate change.\",\n        \"b\": \"Database tracking national climate pledges.\",\n        \"c\": \"Scientific model predicting future climate scenarios.\",\n        \"d\": \"International organization promoting climate action.\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"\\\"Greenwashing\\\" in the context of corporate social responsibility refers to:\",\n      \"options\": {\n        \"a\": \"Companies' actual environmental performance.\",\n        \"b\": \"Companies' misleading claims about their environmental impact.\",\n        \"c\": \"Government regulations on environmental reporting.\",\n        \"d\": \"International standards for environmental sustainability.\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"The Miyawaki method is primarily associated with:\",\n      \"options\": {\n        \"a\": \"Large-scale reforestation projects.\",\n        \"b\": \"Urban afforestation and creating mini-forests.\",\n        \"c\": \"Sustainable agriculture practices.\",\n        \"d\": \"Soil conservation techniques.\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"Biomethanation is most relevant to which sector in India?\",\n      \"options\": {\n        \"a\": \"Agriculture\",\n        \"b\": \"Municipal waste management\",\n        \"c\": \"Industrial wastewater treatment\",\n        \"d\": \"Energy generation\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"The Digital India Land Records Modernisation Programme's main goal is:\",\n      \"options\": {\n        \"a\": \"To digitize all land records in India.\",\n        \"b\": \"To improve land administration in rural areas.\",\n        \"c\": \"To provide land ownership certificates to all citizens.\",\n        \"d\": \"To promote transparency in land transactions.\"\n      },\n      \"answer\": \"a\"\n    },\n    {\n      \"question\": \"The Tea Board in India primarily functions to:\",\n      \"options\": {\n        \"a\": \"Promote tea consumption in India.\",\n        \"b\": \"Regulate the tea industry in India.\",\n        \"c\": \"Export Indian tea to international markets.\",\n        \"d\": \"Provide financial assistance to tea farmers.\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"The Sumed Pipeline is significant for:\",\n      \"options\": {\n        \"a\": \"Transporting oil and gas from the Persian Gulf to Europe.\",\n        \"b\": \"Connecting the Red Sea and the Mediterranean Sea.\",\n        \"c\": \"Providing water to arid regions in the Middle East.\",\n        \"d\": \"Transporting natural gas from Russia to Europe.\"\n      },\n      \"answer\": \"a\"\n    },\n    {\n      \"question\": \"The World Toilet Organization's primary focus is on:\",\n      \"options\": {\n        \"a\": \"Providing toilets in urban areas.\",\n        \"b\": \"Promoting global sanitation initiatives.\",\n        \"c\": \"Funding sanitation projects in developing countries.\",\n        \"d\": \"Manufacturing and distributing toilets worldwide.\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"National Handloom Day in India is celebrated to:\",\n      \"options\": {\n        \"a\": \"Commemorate the invention of the handloom.\",\n        \"b\": \"Promote the use of handloom products.\",\n        \"c\": \"Recognize the contribution of handloom weavers.\",\n        \"d\": \"Protect traditional handloom techniques from extinction.\"\n      },\n      \"answer\": \"c\"\n    },\n    {\n      \"question\": \"The Fractional Orbital Bombardment System (FOBS) is primarily associated with:\",\n      \"options\": {\n        \"a\": \"Space-based missile defense systems.\",\n        \"b\": \"Hypersonic missile technology.\",\n        \"c\": \"Low Earth orbit satellite deployment.\",\n        \"d\": \"Anti-satellite weapon systems.\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"The Nari Shakti Vandan Adhiniyam primarily focuses on:\",\n      \"options\": {\n        \"a\": \"Women's political representation.\",\n        \"b\": \"Women's economic empowerment.\",\n        \"c\": \"Women's health and safety.\",\n        \"d\": \"Reservation for women in government jobs.\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"The Mitra Shakti-2023 military exercise involved:\",\n      \"options\": {\n        \"a\": \"India and China.\",\n        \"b\": \"India and Pakistan.\",\n        \"c\": \"India and Bangladesh.\",\n        \"d\": \"India and Sri Lanka.\"\n      },\n      \"answer\": \"c\"\n    },\n    {\n      \"question\": \"The India Sanitation Coalition is primarily:\",\n      \"options\": {\n        \"a\": \"A government agency.\",\n        \"b\": \"A UN-backed organization.\",\n        \"c\": \"A non-profit organization promoting sustainable sanitation.\",\n        \"d\": \"An international consortium of sanitation companies.\"\n      },\n      \"answer\": \"c\"\n    },\n    {\n      \"question\": \"The National Institute of Urban Affairs primarily focuses on:\",\n      \"options\": {\n        \"a\": \"Urban planning and development.\",\n        \"b\": \"Urban infrastructure development.\",\n        \"c\": \"Urban poverty alleviation.\",\n        \"d\": \"Addressing urban governance challenges.\"\n      },\n      \"answer\": \"a\"\n    },\n    {\n      \"question\": \"The Net-Zero Industry Act, recently passed by the European Parliament, aims to:\",\n      \"options\": {\n        \"a\": \"Reduce carbon emissions from all industries.\",\n        \"b\": \"Promote the use of renewable energy sources.\",\n        \"c\": \"Achieve carbon neutrality by 2040 in the EU.\",\n        \"d\": \"Invest in clean technology development within the EU.\"\n      },\n      \"answer\": \"c\"\n    }\n  ]\n}\n```",
      ],
    },
    {
      "role": "user",
      "parts": [
        files[3],
        "go through this doc on the various subjects that the paper is to be created for . Create questions for the subjects under the header of paper-01, based on ",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Here are 40 multiple-choice questions for the UPSC Prelims exam, categorized by subject area from Paper 01, and designed to be challenging yet realistic in style.  Remember that actual UPSC questions often require deeper analysis and knowledge application than these practice questions.\n\n\n**1. Current Affairs Analysis and Questions:**\n\n1.  Which country recently hosted the G20 Summit?\n    (a) India  (b) Indonesia  (c) China  (d) Brazil\n\n2.  What major international agreement was recently signed to address climate change?\n    (a) Kyoto Protocol (b) Paris Agreement (c) Montreal Protocol (d)  Copenhagen Accord\n\n3.  Which significant global economic event dominated headlines recently?\n    (a)  A major currency devaluation (b) A significant interest rate hike (c) A major stock market crash (d) A global recession\n\n4.  A recent major geopolitical event involved which two countries? (choose the most significant recent event)\n    (a)  India and Pakistan (b) Russia and Ukraine (c) China and Taiwan (d) USA and Iran\n\n5.  What significant development recently occurred in the field of space exploration?\n    (a) A new space telescope launch (b) A successful moon landing (c) A Mars rover discovery (d) A new space station module\n\n**2. History of India and Indian National Movement:**\n\n6.  The Partition of India resulted in the creation of which two nations?\n    (a) India and Pakistan (b) India and Bangladesh (c) India and Sri Lanka (d) Pakistan and Afghanistan\n\n7.  Which movement significantly challenged British rule in India in the early 20th century?\n    (a) Sepoy Mutiny (b) Non-Cooperation Movement (c) Quit India Movement (d)  Swadeshi Movement\n\n8.  Who is considered the \"Father of Modern India\"?\n    (a)  Mahatma Gandhi (b) Jawaharlal Nehru (c) Sardar Vallabhbhai Patel (d)  Raja Ram Mohan Roy\n\n9.  The Dandi March was a significant event in which major movement?\n    (a)  Quit India Movement (b) Non-Cooperation Movement (c) Civil Disobedience Movement (d)  Salt Satyagraha\n\n10. Which historical figure played a crucial role in India's independence struggle through diplomacy and international relations?\n     (a) Jawaharlal Nehru (b) Sardar Vallabhbhai Patel (c) Mahatma Gandhi (d) Subhas Chandra Bose\n\n\n**3. Indian and World Geography:**\n\n11. Which mountain range is located in the Eastern Himalayas?\n     (a) Karakoram (b) Patkai Bum (c) Arakan Yoma (d)  Himalayas\n\n12. The longest river in India is:\n     (a) Ganga (b) Brahmaputra (c) Godavari (d)  Yamuna\n\n13. Which of these is a major hot desert?\n     (a) Thar Desert (b) Sahara Desert (c) Arabian Desert (d)  Gobi Desert\n\n14. Which geographical feature is known for its unique biodiversity?\n     (a) Sundarbans (b) Amazon Rainforest (c) Great Barrier Reef (d)  Galapagos Islands\n\n15. The largest plateau in India is:\n     (a) Deccan Plateau (b) Malwa Plateau (c) Chota Nagpur Plateau (d)  Chotanagpur Plateau\n\n\n**4. Indian Polity and Governance:**\n\n16. The Indian Constitution is based on which principle?\n     (a) Unitary (b) Federal (c) Presidential (d)  Parliamentary\n\n17. Which schedule of the Indian Constitution deals with languages?\n     (a) 1st (b) 6th (c) 8th (d)  12th\n\n18. The concept of \"Directive Principles of State Policy\" is found in which part of the Indian Constitution?\n     (a) Part III (b) Part IV (c) Part IV A (d)  Part V\n\n19. The Indian Constitution guarantees which fundamental right?\n     (a) Right to work (b) Right to education (c) Right to property (d)  Right to equality\n\n20. Which institution is responsible for the appointment of the Chief Election Commissioner of India?\n     (a) Parliament (b) President (c) Prime Minister (d)  Supreme Court\n\n\n**5. Economic and Social Development:**\n\n21. What is the Human Development Index (HDI)?\n     (a) A measure of economic growth.  (b) A measure of a country's overall development. (c) A measure of industrial output. (d) A measure of literacy rates.\n\n22. Which of the following is a major challenge to sustainable development?\n     (a) Technological advancements (b) Climate change (c) Population growth (d)  Resource depletion\n\n23. What is the main objective of the National Food Security Act?\n     (a) To increase agricultural production (b) To ensure food security for all citizens (c) To promote export of food grains (d)  To regulate food prices\n\n24. Which of the following is a significant social sector initiative in India?\n     (a)  National Rural Health Mission (b) Mahatma Gandhi National Rural Employment Guarantee Act (c) Pradhan Mantri Jan Dhan Yojana (d)  Swachh Bharat Abhiyan\n\n25. A key aspect of social inclusion in India focuses on:\n     (a)  Economic growth (b) Educational opportunities (c) Empowering marginalized communities (d)  Infrastructure development\n\n\n**6. General Issues on Environmental Ecology, Biodiversity and Climate Change:**\n\n26. What is the primary cause of ozone depletion?\n     (a)  Carbon dioxide emissions (b) Chlorofluorocarbons (CFCs) (c) Methane emissions (d)  Deforestation\n\n27. Which protocol is primarily associated with the reduction of greenhouse gas emissions?\n     (a) Montreal Protocol (b) Kyoto Protocol (c) Paris Agreement (d)  Copenhagen Accord\n\n28. What is biodiversity?\n     (a) The variety of life on Earth (b) The number of species in a region (c) The genetic diversity within a species (d)  The distribution of species across the globe\n\n29. Which of the following is a major threat to biodiversity?\n     (a) Climate change (b) Habitat loss (c) Pollution (d)  Overexploitation of resources\n\n30. What is the main aim of the Ramsar Convention?\n     (a) To protect endangered species (b) To conserve wetlands (c) To combat desertification (d)  To promote sustainable agriculture\n\n\n**7. General Science and Technology:**\n\n31. What is the primary function of a \"bioreactor\" in biotechnology?\n     (a) To produce vaccines (b) To grow microorganisms (c) To synthesize proteins (d)  To purify DNA\n\n32. What is nanotechnology?\n     (a) The study of extremely small organisms (b) The science of manipulating materials at the atomic level (c) The science of creating artificial intelligence (d)  The study of the universe\n\n33. What is a \"fuel cell\"?\n     (a) A type of battery (b) A device that converts chemical energy into electrical energy (c) A type of engine (d)  A type of generator\n\n34. What is the primary application of \"remote sensing\" technology?\n     (a) Weather forecasting (b) Military surveillance (c) Environmental monitoring (d)  Medical imaging\n\n35. What is CRISPR technology primarily used for?\n     (a) Gene editing (b) Cloning (c) Stem cell research (d)  Artificial intelligence\n\n\nThis set of questions aims to provide a broad range of topics and difficulty levels, reflecting the diverse nature of the UPSC Prelims exam.  Remember to consult official UPSC resources and materials for the most accurate and up-to-date information.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "keep the response as json please\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\n  \"questions\": [\n    {\n      \"question\": \"Which country recently hosted the G20 Summit?\",\n      \"options\": {\n        \"a\": \"India\",\n        \"b\": \"Indonesia\",\n        \"c\": \"China\",\n        \"d\": \"Brazil\"\n      },\n      \"answer\": \"a\" \n    },\n    {\n      \"question\": \"What major international agreement was recently signed to address climate change?\",\n      \"options\": {\n        \"a\": \"Kyoto Protocol\",\n        \"b\": \"Paris Agreement\",\n        \"c\": \"Montreal Protocol\",\n        \"d\": \"Copenhagen Accord\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"Which significant global economic event dominated headlines recently?\",\n      \"options\": {\n        \"a\": \"A major currency devaluation\",\n        \"b\": \"A significant interest rate hike\",\n        \"c\": \"A major stock market crash\",\n        \"d\": \"A global recession\"\n      },\n      \"answer\": \"d\"\n    },\n    {\n      \"question\": \"A recent major geopolitical event involved which two countries? (choose the most significant recent event)\",\n      \"options\": {\n        \"a\": \"India and Pakistan\",\n        \"b\": \"Russia and Ukraine\",\n        \"c\": \"China and Taiwan\",\n        \"d\": \"USA and Iran\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"What significant development recently occurred in the field of space exploration?\",\n      \"options\": {\n        \"a\": \"A new space telescope launch\",\n        \"b\": \"A successful moon landing\",\n        \"c\": \"A Mars rover discovery\",\n        \"d\": \"A new space station module\"\n      },\n      \"answer\": \"a\"\n    },\n    {\n      \"question\": \"The Partition of India resulted in the creation of which two nations?\",\n      \"options\": {\n        \"a\": \"India and Pakistan\",\n        \"b\": \"India and Bangladesh\",\n        \"c\": \"India and Sri Lanka\",\n        \"d\": \"Pakistan and Afghanistan\"\n      },\n      \"answer\": \"a\"\n    },\n    {\n      \"question\": \"Which movement significantly challenged British rule in India in the early 20th century?\",\n      \"options\": {\n        \"a\": \"Sepoy Mutiny\",\n        \"b\": \"Non-Cooperation Movement\",\n        \"c\": \"Quit India Movement\",\n        \"d\": \"Swadeshi Movement\"\n      },\n      \"answer\": \"d\"\n    },\n    {\n      \"question\": \"Who is considered the \\\"Father of Modern India\\\"?\",\n      \"options\": {\n        \"a\": \"Mahatma Gandhi\",\n        \"b\": \"Jawaharlal Nehru\",\n        \"c\": \"Sardar Vallabhbhai Patel\",\n        \"d\": \"Raja Ram Mohan Roy\"\n      },\n      \"answer\": \"d\"\n    },\n    {\n      \"question\": \"The Dandi March was a significant event in which major movement?\",\n      \"options\": {\n        \"a\": \"Quit India Movement\",\n        \"b\": \"Non-Cooperation Movement\",\n        \"c\": \"Civil Disobedience Movement\",\n        \"d\": \"Salt Satyagraha\"\n      },\n      \"answer\": \"d\"\n    },\n    {\n      \"question\": \"Which historical figure played a crucial role in India's independence struggle through diplomacy and international relations?\",\n      \"options\": {\n        \"a\": \"Jawaharlal Nehru\",\n        \"b\": \"Sardar Vallabhbhai Patel\",\n        \"c\": \"Mahatma Gandhi\",\n        \"d\": \"Subhas Chandra Bose\"\n      },\n      \"answer\": \"a\"\n    },\n    {\n      \"question\": \"Which mountain range is located in the Eastern Himalayas?\",\n      \"options\": {\n        \"a\": \"Karakoram\",\n        \"b\": \"Patkai Bum\",\n        \"c\": \"Arakan Yoma\",\n        \"d\": \"Himalayas\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"The longest river in India is:\",\n      \"options\": {\n        \"a\": \"Ganga\",\n        \"b\": \"Brahmaputra\",\n        \"c\": \"Godavari\",\n        \"d\": \"Yamuna\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"Which of these is a major hot desert?\",\n      \"options\": {\n        \"a\": \"Thar Desert\",\n        \"b\": \"Sahara Desert\",\n        \"c\": \"Arabian Desert\",\n        \"d\": \"Gobi Desert\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"Which geographical feature is known for its unique biodiversity?\",\n      \"options\": {\n        \"a\": \"Sundarbans\",\n        \"b\": \"Amazon Rainforest\",\n        \"c\": \"Great Barrier Reef\",\n        \"d\": \"Galapagos Islands\"\n      },\n      \"answer\": \"a\"\n    },\n    {\n      \"question\": \"The largest plateau in India is:\",\n      \"options\": {\n        \"a\": \"Deccan Plateau\",\n        \"b\": \"Malwa Plateau\",\n        \"c\": \"Chota Nagpur Plateau\",\n        \"d\": \"Chotanagpur Plateau\"\n      },\n      \"answer\": \"a\"\n    },\n    {\n      \"question\": \"The Indian Constitution is based on which principle?\",\n      \"options\": {\n        \"a\": \"Unitary\",\n        \"b\": \"Federal\",\n        \"c\": \"Presidential\",\n        \"d\": \"Parliamentary\"\n      },\n      \"answer\": \"d\"\n    },\n    {\n      \"question\": \"Which schedule of the Indian Constitution deals with languages?\",\n      \"options\": {\n        \"a\": \"1st\",\n        \"b\": \"6th\",\n        \"c\": \"8th\",\n        \"d\": \"12th\"\n      },\n      \"answer\": \"c\"\n    },\n    {\n      \"question\": \"The concept of \\\"Directive Principles of State Policy\\\" is found in which part of the Indian Constitution?\",\n      \"options\": {\n        \"a\": \"Part III\",\n        \"b\": \"Part IV\",\n        \"c\": \"Part IV A\",\n        \"d\": \"Part V\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"The Indian Constitution guarantees which fundamental right?\",\n      \"options\": {\n        \"a\": \"Right to work\",\n        \"b\": \"Right to education\",\n        \"c\": \"Right to property\",\n        \"d\": \"Right to equality\"\n      },\n      \"answer\": \"d\"\n    },\n    {\n      \"question\": \"Which institution is responsible for the appointment of the Chief Election Commissioner of India?\",\n      \"options\": {\n        \"a\": \"Parliament\",\n        \"b\": \"President\",\n        \"c\": \"Prime Minister\",\n        \"d\": \"Supreme Court\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"What is the Human Development Index (HDI)?\",\n      \"options\": {\n        \"a\": \"A measure of economic growth.\",\n        \"b\": \"A measure of a country's overall development.\",\n        \"c\": \"A measure of industrial output.\",\n        \"d\": \"A measure of literacy rates.\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"Which of the following is a major challenge to sustainable development?\",\n      \"options\": {\n        \"a\": \"Technological advancements\",\n        \"b\": \"Climate change\",\n        \"c\": \"Population growth\",\n        \"d\": \"Resource depletion\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"What is the main objective of the National Food Security Act?\",\n      \"options\": {\n        \"a\": \"To increase agricultural production\",\n        \"b\": \"To ensure food security for all citizens\",\n        \"c\": \"To promote export of food grains\",\n        \"d\": \"To regulate food prices\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"Which of the following is a significant social sector initiative in India?\",\n      \"options\": {\n        \"a\": \"National Rural Health Mission\",\n        \"b\": \"Mahatma Gandhi National Rural Employment Guarantee Act\",\n        \"c\": \"Pradhan Mantri Jan Dhan Yojana\",\n        \"d\": \"Swachh Bharat Abhiyan\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"A key aspect of social inclusion in India focuses on:\",\n      \"options\": {\n        \"a\": \"Economic growth\",\n        \"b\": \"Educational opportunities\",\n        \"c\": \"Empowering marginalized communities\",\n        \"d\": \"Infrastructure development\"\n      },\n      \"answer\": \"c\"\n    },\n    {\n      \"question\": \"What is the primary cause of ozone depletion?\",\n      \"options\": {\n        \"a\": \"Carbon dioxide emissions\",\n        \"b\": \"Chlorofluorocarbons (CFCs)\",\n        \"c\": \"Methane emissions\",\n        \"d\": \"Deforestation\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"Which protocol is primarily associated with the reduction of greenhouse gas emissions?\",\n      \"options\": {\n        \"a\": \"Montreal Protocol\",\n        \"b\": \"Kyoto Protocol\",\n        \"c\": \"Paris Agreement\",\n        \"d\": \"Copenhagen Accord\"\n      },\n      \"answer\": \"c\"\n    },\n    {\n      \"question\": \"What is biodiversity?\",\n      \"options\": {\n        \"a\": \"The variety of life on Earth\",\n        \"b\": \"The number of species in a region\",\n        \"c\": \"The genetic diversity within a species\",\n        \"d\": \"The distribution of species across the globe\"\n      },\n      \"answer\": \"a\"\n    },\n    {\n      \"question\": \"Which of the following is a major threat to biodiversity?\",\n      \"options\": {\n        \"a\": \"Climate change\",\n        \"b\": \"Habitat loss\",\n        \"c\": \"Pollution\",\n        \"d\": \"Overexploitation of resources\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"What is the main aim of the Ramsar Convention?\",\n      \"options\": {\n        \"a\": \"To protect endangered species\",\n        \"b\": \"To conserve wetlands\",\n        \"c\": \"To combat desertification\",\n        \"d\": \"To promote sustainable agriculture\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"What is the primary function of a \\\"bioreactor\\\" in biotechnology?\",\n      \"options\": {\n        \"a\": \"To produce vaccines\",\n        \"b\": \"To grow microorganisms\",\n        \"c\": \"To synthesize proteins\",\n        \"d\": \"To purify DNA\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"What is nanotechnology?\",\n      \"options\": {\n        \"a\": \"The study of extremely small organisms\",\n        \"b\": \"The science of manipulating materials at the atomic level\",\n        \"c\": \"The science of creating artificial intelligence\",\n        \"d\": \"The study of the universe\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"What is a \\\"fuel cell\\\"?\",\n      \"options\": {\n        \"a\": \"A type of battery\",\n        \"b\": \"A device that converts chemical energy into electrical energy\",\n        \"c\": \"A type of engine\",\n        \"d\": \"A type of generator\"\n      },\n      \"answer\": \"b\"\n    },\n    {\n      \"question\": \"What is the primary application of \\\"remote sensing\\\" technology?\",\n      \"options\": {\n        \"a\": \"Weather forecasting\",\n        \"b\": \"Military surveillance\",\n        \"c\": \"Environmental monitoring\",\n        \"d\": \"Medical imaging\"\n      },\n      \"answer\": \"c\"\n    },\n    {\n      \"question\": \"What is CRISPR technology primarily used for?\",\n      \"options\": {\n        \"a\": \"Gene editing\",\n        \"b\": \"Cloning\",\n        \"c\": \"Stem cell research\",\n        \"d\": \"Artificial intelligence\"\n      },\n      \"answer\": \"a\"\n    }\n  ]\n}\n```",
      ],
    },
  ]
)

response = chat_session.send_message("give me the content of the first uploaded file") # input a prompt like specific subject qs or more qs
# fine tune a model o sepcify the formatting of the output string that is to be obtained 
"""def save_response_to_json(response_data, file_path):
    import json

    try:
        if hasattr(response_data, 'to_dict'):
            response_data = response_data.to_dict()
        else:
            response_data = response_data.__dict__

        with open(file_path, 'w') as json_file:
            json.dump(response_data, json_file, indent=4)
        print(f"Response saved to {file_path}")
    except Exception as e:
        print(f"Error saving response to JSON: {e}")

save_response_to_json(response, "response_data.json")

"""

print(response.text)

























































































































































































































