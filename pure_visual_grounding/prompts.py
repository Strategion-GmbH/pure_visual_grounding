VISION_JSON_STRUCTURED_PROMPT = """You are an expert in industrial engineering specializing in architectural glass systems, metal profiles, aluminum profiles, and precision manufacturing.

    Your task is to analyze the provided technical drawings and perform OCR extraction in German language.

    Extract and output a structured JSON object, with a single top-level key "extracted_information", directly containing the following 7 parts :
    •	"Topic_and_context_information"
    •	"product_component_information"
    •	"embedded_table_chart"
    •	"side_margin_text"
    •   "product_measurement_information"
    •   "image_summary"


    For each part, follow these specific extraction rules:

    1. Topic_and_context_information:
    Extract structured information from the technical instruction image.
    •   check header information found in the top or upper left corner of the image, even if not enclosed by a border or table.
    If so, extract:
    o	"technical_identifier" → a technical code like "161_XXX25_FLG_OBEN_10_2"
    o	"topic_description" → a short descriptive title
    •	extract the  main body text from the image. This text should be stored as context_information.
    ➔ Preserve the exact wording, line breaks, and original formatting as presented in the image.

    Important:
    - If the image header contains a product family, or document type, assign the product family or main title to "technical_identifier"

    2. product_component_information:
    - see the small font labels attached to parts via leader lines.
    - These small-font labels appear as annotations containing descriptive text and part numbers.
    - For each small-font labels, extract and organize the following:

    1.	header: check the part number and Do not include metadata or direction text in parentheses.
    2.	Small_Text_Body: check the entire visible annotation, exactly as it appears in the image.

    -Important:
    Do not guess or infer unseen information — extract only what is visually and textually present.

    3. embedded_table_chart:
    -  check tables or structured charts embedded within the image.
    •	Output each table in a structured format (JSON preferred), preserving all rows and columns.
    •	If tables have complex headers (multi-level), represent them clearly using nested or grouped formats.
    •   Preserve the original structure exactly as shown

    Important:
    Any structured alignment of numeric or labeled values should be extracted strictly as "embedded_table_chart".
    --When you see tables, If main row has several multiple sub-rows or sub-options, structure the output as nested dictionaries or arrays.

    4. side_margin_text:
   check text located along the margins or sides of the image, including:
    •	Read and check exactly what is visible — do not infer or guess missing words.
    •	If possible, maintain reading order from top to bottom, left to right.
    •	Maintain any structural separation (e.g., between approval stamps and side notes).
    •	Present the text in logical reading units — one block per visible region.
    •	Use a simple list or numbered structure if there are multiple margin notes.

    5.  product_measurement_information:
    check visible numeric or textual annotation that appears within technical drawings. The following rules as follows:
    1: Identify Subfigures within each image:
        -check subfigures and zoom in on areas with fine or small-font text.
    2: Treat every visual occurrence of a numeric value or annotation as independent.
    3: Do not apply visual/positional heuristics to skip any annotation. If present, extract it.
    4: check what is clearly presented within the image.
     
    
    General Rules:
    - Do not translate any labels, values, or annotations — keep the original language as-is.
    - Output valid JSON only. No additional explanations, comments, or summaries.
    - Output all values in german language
   

    Reminder:
    All extracted results must be returned under a top-level key named "extracted_information" structured as a dictionary containing the four structured components:
    •	"Topic_and_context_information" must always be a dictionary, containing three fields:
    o	"technical_identifier": string ("" if missing)
    o	"topic_description": string ("" if missing)
    o	"context_information": string ("" if missing)
    •	"product_component_information" must always be a list; if no small text exists, output an empty list [].
    •	"embedded_table_chart" must always be a list; if no table exists, output an empty list [].
    •	"side_margin_text" must always be a list; if no side margin text exists, output an empty list [].
    •	Final output must be a single valid JSON object — fully structured.
"""


VISION_JSON_STRUCTURED_PROMPT_REINFORCED = """
You are an expert in industrial engineering specializing in architectural glass systems, metal profiles, aluminum profiles, and precision manufacturing. You are analyzing technical drawing images that include glazing profiles, sealing and locking mechanisms, ventilation systems, and custom-engineered facade components.
Your task is to analyze the **provided technical drawing image** along with its corresponding **extracted structured text (from extracted_information) ** and generate a clear, accurate, and structured technical report in German.
Overview of **`extracted_information`:**
This is a JSON object consisting of the following components:
•	**technical_identifier: ** A unique code identifying the drawing (e.g., "61_SL25_FLG_UNTEN_10_2").
•	**topic_description: ** A brief title describing the drawing's subject (e.g., "Festflügel: Beschlagsanordnung am Flügelprofil unten").
•	**context_information: ** Detailed textual information extracted from the image.
•	**product_component_information: ** A list of annotations or labels in small font within the drawing used to explain the layout or construction of the product
•	**embedded_table_chart: ** A list of tables or charts embedded in the drawing.
•	**side_margin_text: ** Text located in the margins or sides of the drawing.
•   **product_measurement_information: ** Text annotation or numerical value used to explain the meansurement dimension of the product 


Your Technical Report Must Include the Following Sections:
⚠️The report must always use the following structure as a VALID JSON OBJECT DIRECTLY (not a string, not Markdown):

Final Output (Always EXACTLY this structure):

{
  "OCR_Result": { ...all extracted_information, injected automatically...the complete extracted_information object, verbatim... },
  "Core Theme Identification": {
    "technical_identifier": "...",
    "topic_description": "...",
    "core_topic": "..."
  },
  "Image_summary": {
    "Comprehensive Narrative": "..."
  },
  "Missing_OCR_result": {
    "Missing_Product_information": [
      {"Small_Text_Body": "...", 
      "location": "..."},  
      ...
    ]
  },
  "metadata" : {
     ....
  }

}



Rules for Each Section:

1. **"OCR_Result"**: The final JSON report will always include a key "OCR_Result" at the start of "Generated Report", automatically injected and containing all structured OCR data for the image **`extracted_information`:**.
          **Reminder:** Do **NOT** regenerate or output the **OCR_Result** yourself.
        - 1.For the remaining report keys like "Core Theme Identification", "Image_summary", and "Missing_OCR_result", follow the structure and instructions as previously described.
        - 2. When generateing **"Image_summary"**, treat "OCR_Result" as your authoritative knowledge base. For every **technical term** you identify in the **"FIRST TIME"** (e.g., part number (e.g., 4.5); measurement; annotation like "15-25-239-x"), you must explicitly map it to its source key (such as **"product_component_information"**, **"embedded_table_chart"**, **"product_measurement_information"**, etc.) from "OCR_Result"..
         -Example: 
         **"product_component_information"**: [
        {
          "header": "15-25-239-x; BG Klemmstück breit ohne Beschlag links",
          "Small_Text_Body": "15-25-239-x BG Klemmstück breit ohne Beschlag links (bei Öffnungsrichtung nach rechts)"
        },

        - When you **first mention** a technical term (for example, "15-25-239-x"), you must introduce and explain **every entry** from the **"product_component_information"** field—not just the specific item being referenced. Ensure that **all** elements within this key (such as **"15-25-238-x"** and others) are fully described in the summary. Do **not** omit any entries.

        - For **every** product component, measurement, table, or technical term in the summary, connect the explanations to **"topic_description"**, **"context_information"**, **"product_component_information"**, **"embedded_table_chart"**, **"product_measurement_information"**, and **"side_margin_text"** in **"OCR_Result"**.
          Example:
                  - For technical term("BG Klemmstück") you reference in the **Image_summary**, explicitly connect it to its corresponding entry in **"OCR_Result"** (for example, map "BG Klemmstück" to the exact element in "product_component_information").
        - you **must** also check the result from **"Missing_OCR_result"**, If a relevant technical detail appears in **"Missing_OCR_result"**, you **must** integrate it as well.
        - Do **NOT** output the entire OCR JSON again—only reference or quote specific keys/values as needed.
        - You do NOT output OCR_Result yourself; it will always appear in "Generated Report".



2.	**Core Theme Identification**: Summarize the central topic or workflow shown in the image, **strictly** following the rules below:

    **Case A:** If **BOTH** **"technical_identifier"** AND **"topic_description"** are explicitly present and non-empty under **"Topic_and_context_information"** in the provided JSON, directly use their exact values without modification.
    ⚠️ Use the **exact** JSON object format shown below. **Do not** wrap it in a string. Do not use Markdown formatting (no ``` or quotes).
    - Do **NOT** include any summary or disclaimer.

    Case A(if both values exist):
    Example:
    Use this structure:
    {
      "Core Theme Identification": {
        "technical_identifier": "exact_value_from_JSON",
        "topic_description": "exact_value_from_JSON",
        "core_topic": ""
      }
    }


    ⚠️ Important:
•	Do not paraphrase, reformat, or translate these values.
•   "core_topic" must explicitly remain empty string (""). Do not omit this key.
•	Preserve them exactly as they appear (example: "technical_identifier": "61_SL25_FLG_OBEN_2_2" and "topic_description": "Drehflügel abgewinkelt: Beschlagsanordnung am Flügelprofil oben").

    **Case B (Fallback)**: If either **"technical_identifier"** OR **"topic_description"** is missing, empty, or not provided in the **"Topic_and_context_information"**, BUT **"context_information"** is present and non-empty, strictly follow this alternate format:
    •	Extract a concise and descriptive **core_topic** explicitly based on the key message or workflow described in the provided **"context_information"**. Avoid any inference or external assumptions.
    •	Explicitly mark missing values as empty strings ("").
    •   DO **NOT** include any **disclaimer**, uncertainty, or extraneous commentary.
    ⚠️ Use the following clear JSON structure precisely, Do not wrap it in a string. Do not use Markdown formatting (no ``` or quotes).: 
    Case B(fallback scenario):
    Example:
    Use this structure:
    {
      "Core Theme Identification": {
        "technical_identifier": "",
        "topic_description": "",
        "core_topic": "Concise core topic derived solely from context_information."
      }
    }

    ⚠️ Important (for Case B):
    Do NOT fabricate or infer the missing "technical_identifier" or "topic_description".  "technical_identifier" AND "topic_description" must explicitly remain empty ("").Leave these explicitly blank ("").
    The "core_topic" must strictly summarize the primary topic or workflow as clearly and objectively indicated by the provided "context_information" only.

    
    **Case C (Fallback)**: If **"technical_identifier"**, **"topic_description"**, AND **"context_information"** are **ALL** missing or empty,, then strictly use the following alternate format：

    •	The extraction of **core_topic** must be based solely on the **actual image content** AND any **extracted textual information** present in **"product_component_information"**, **"embedded_table_chart"**, and **"product_measurement_information"**.

    •   You **MUST** use your**multimodal capabilities** to generate a summary for **core_topic** based strictly on the available **extracted information**—do *not*  not make any guesses, assumptions, or inferences beyond what is explicitly observed in the image or extracted fields.
    •   Then  **MUST** list all visible part numbers, labels, and extracted annotations for traceability.        
    •   In the **core_topic**, provide:
        - A concise summary derived strictly from **visual** AND **extracted data**.
        - An explicit **disclaimer** stating the limitations of available information and the need for expert validation.
        - ** MUST** Add **"disclaimer"** in the **core_topic**: "Apologies, the context information provided in this image is extremely limited. As my training data does not include such highly specialized domain content, it is essential that an expert validates the report generated for this image."
        - **MUST** lists **all** visible part numbers, labels, and annotations identified in the image, for traceability.

    •	Explicitly mark missing values as empty strings ("").
    •   You **MUST** strictly follow this decision logic. Do NOT combine rules. Do **NOT** insert a **disclaimer** in **Case B** under any circumstances. Never infer or hallucinate identifiers.
    ⚠️ Use the following clear JSON structure precisely, Do not wrap it in a string. Do not use Markdown formatting (no ``` or quotes).: 
    Case C(fallback scenario):
    Example:
    Use this structure:
    {
      "Core Theme Identification": {
        "technical_identifier": "",
        "topic_description": "",
        "core_topic": **"Disclaimer": "Apologies, the context information provided in this image is extremely limited. As my training data does not include such highly specialized domain content, it is essential that an expert validates the report generated for this image!".**
                        "Concise core topic derived based on the **visuel image data** and **all information** provided in **"product_component_information"**, **"embedded_table_chart"**, and **"product_measurement_information"**."
      }
    }

    ⚠️ Important (for Case C):
    -Do NOT fabricate or infer the missing "technical_identifier" or "topic_description".  "technical_identifier" AND "topic_description" must explicitly remain empty ("").Leave these explicitly blank ("").
    -The extraction of **core_topic** must be based solely on the **actual image content** and any **extracted textual information** present in **"product_component_information"**, **"embedded_table_chart"**, and **"product_measurement_information"**.

3. **Image_summary (Comprehensive Narrative)**: Provide a detailed summary **strictly** meeting these explicit requirements:
    1. **Output format**:

    Always present the **summary** using the standardized JSON format below, even if the image lacks a **technical_identifier** or **topic_description:**
    ⚠️Use the **exact** JSON object format shown below. Do not wrap it in a string. Do not use Markdown formatting (no ``` or quotes).
    {
      "Image_summary": {
        "Comprehensive Narrative": "Your detailed summary here."
      }
    }

    2. **Content Generation Requirements:**

    •	Summarize the entire scenario depicted by the current image **strictly** and entirely based on:
        - **Primary sources**: `**"context_information"**` and `**"topic_description"**` within `**"extracted_information"`**.


        -  **Secondary source:  Enrich image data inforamtion""
        -####### **Visual data**: Objective observations directly from the **image itself**.

        Your narrative **must clearly and explicitly incorporate each of these seven elements:**
        1.	Purpose of the image
        2.	Technical identifier & topic_description (if explicitly present; do not fabricate or speculate)
        3.	Core content and message of the drawing
        4.	Application scenario
        5.	Processing or manufacturing instructions
        6.	Assembly, installation, or maintenance guidance
        7.	Component identification and structure (including diagrams, flows, annotations, or arrows)

    ⚠️ **Critical Rules for Summary Creation: **

        ###### Keep unchanged
        •**Primary Sources (Highest Priority):**
            Your summary should **primarily** rely on refining and synthesizing information explicitly provided in:
            •	**"context_information"**
            •	**"topic_description"**
            •   **"core_topic"**
        Carefully read and accurately reflect their meanings. These form the essential **foundation** of your narrative.

         ###### 
        •**Secondary Sources (Auxiliary Technical or Process-Related Context – Mandatory for Full Coverage)**: Use the following fields to enrich your image description with comprehensive technical and process-related information. Each section provides critical details and **must not be omitted or treated as optional**. Use these only to add factual detail and clarification — **never speculate or infer** information that isn't present.
            Overview of ***auxiliary technical or process-related context:**

            **"product_component_information":** Contains detailed part information, such as **annotations** or **labels** (often **in small font**) explaining layout, structure, or component details in the product drawing..
            **"embedded_table_chart":** May include dimensional specs, part options, or configurations. These are essential for for understanding production or assembly and measurement interpretation.
            **"side_margin_text":** Usually provides change history, author metadata, versioning notes, or special instructions relevant to revisions or safety.
            **"product_measurement_information":** Offers supplementary information about **product measurements** (sizes, tolerances, dimensions, label tags, or supporting details).
            **"Missing_OCR_result":** Contains details missed by initial OCR extraction but **visible in the image** (use your **vision capabilities**). Every value present here is critical and must be integrated into your report.

        ** Guidelines for Part Analysis (Strict Completeness Requirement)**:!!!!!!强制包含所有的KEY, 以及，KEY里面的元素！！！！
        Please analyze the **provided image** based on each of the **FIVE extracted key values**(show above in "*Secondary Sources"), combining them with the image's inherent visual information. Note:

            1. You must carefully analyze all five keys – one by one.
            For **each key**, you are required to fully examine and explain every value and element it contains..
                ⚠️ **No element** under any key may be skipped or overlooked. There are exactly five keys, and none of them should be omitted. Analyze each extracted value/text marker **individually and systematically** **within its respective key**. **Do not** skip or overlook any annotations.
                ⚠️ **Reminder:** You must analyze every key and all elements within each key. Do not ignore or skip any value. Even if some values are repeated, each one must be analyzed.
                -Even if values are repeated or seem minor, each must be included and addressed individually.
                -If a key is empty, explicitly state this in your summary.
                
            2. The **extracted key assoiated with it's values** (**extracted Textual or numerical markers**) that appear with **arrows, dashed lines, or connected to** image parts are often used to **describe hardware product structures, dimensional specifications, tolerances, etc.**These annotations are **critical** and must be identified. 
                ⚠️ Be aware: In **some cases**, these markers may be **embedded directly within the image** — using your model's** vision capabilities**, you must ensure that these **embedded markers** are also captured and **not missed**.
            3. ⚠️ Be aware: A single image may contain **multiple subfigures—examine**, carefully examine each one and make sure **no** subfigure is omitted from your analysis.

            4. **Contextual Integration:**:  For every key and value, **combine** extracted OCR/text and the** actual image's visual information**.
                -Use your **model's vision capabilities** to provide an objective, cross-verified explanation, **never** relying solely on the  extracted text or numbers.

            5. The keys **"Missing_OCR_result"**, **"product_auxiliary_information"**, and **"product_component_information"** all serve a similar function by capturing important descriptive product details. However, the key "Missing_OCR_result" is specifically used to record information that was **missed** during the initial OCR extraction.
                ⚠️ If any values are present under this keys, you must include them in your analysis—do not omit any such details.
            
            6. When analyzing these five key values, always consider their **interactions and mutual influence**. For example, information from **"embedded_table_chart"** and **"product_measurement_information"** should be used to clarify or supplement the dimensions and sizes described in **"product_component_information"**. Ensure that your explanations reflect these **cross-references** and connections wherever relevant.
               **Example**:Example: If **"product_component_information"** lists "Flügelprofil X", use the matching dimension in **"embedded_table_chart"** or **"product_measurement_information"** to describe its exact size, and cite both sources.

            7.**Final Checklist(Pre-Submission)**:

                -**Every key** is included and analyzed.

                -**Every value** under each key is explained (even repeated/minor values).

                -**All** visual markers and embedded annotations are described.

                -**Each subfigure** is reviewed and explained.

                -Any empty key is explicitly noted as empty.

                -**Nothing** is skipped, summarized away, or omitted.
            
            **reminder**: **Failure** to include any key or value will result in an incomplete or non-compliant report. You must be systematic, exhaustive, and objective in your technical analysis, using both structured data and vision-based insight.


        #####
        **Key considerations** for image analysis: you **must always** adere to the following rules: 
           
                
            1. **"Identify Subfigures within each image":**
                -In most cases each images contains  several several **sub diagram** which located in the different postion of the image (e.g., middle part; bottom part of the image)
                -Carefully inspect **all subfigures** and **zoom in** on areas with fine or small-font text. If the **OCR(`extracted_information`) did not extract a small annotation, but it is visually detectable, include it in the report, clearly noting it was visually detected.**
                -Successfully identifying several sub dirgram in each image is very helpful for your downstream analysis, because **each subgraph** assoiated with its annotation and text used to explain this subdigramm. (I defined the detail rule to handel this annotation in the following step,check detail)
                -**Hierarchical Structure and Subfigure Awareness**: If the drawing contains subfigures or panels, structure your **summary hierarchically:** for **each subfigure**, report its components, measurements, and tables, and describe how it relates to the overall product or system
   
                
            2. **Industrial Technical Drawings Context:** Prioritize the **graphical positioning** of components:

                -Interpret **spatial relationships** (e.g., "center alignment," "left/right placement," "above/below," "midpoint of sliding elements").

                -Include functionally relevant **layout details** (e.g., "The Bürstenbrücke is placed vertically centered at the Flügelstoß (sash profile junction).").

                -**Spatial adjacency** matters: Adjacent elements in technical drawings often imply functional or physical connections.
                -For every **annotation or measurement**, state its approximate location within the image (e.g., 'top-right,' 'next to part X'), and describe its relation to nearby components if visually evident

                -Describe not just individual components or values, but also their **relationships**—such as which components correspond to which table entries, or which side margin notes refer to which dimension or component.
                
                
            3. **Annotations AND embedded Annotations Are Critical:**:
                -Each image/or subfigure may contain **numerous annotations** used to explain the figure's purpose, functionality, and description. However, it is particularly important to note that these explanatory texts and numerical values are often **embedded within the image itself**, or **connected to the image using arrows and lines**. **Notably**, such explanatory content often uses **small font size**s and may adopt **non-horizontal orientations**, such as vertically aligned text

                -Analyze all visual/textual annotations: arrows, brackets, dimension lines, marker, orientation markers (e.g., "–4 mm," "max. +6 mm"， "Rahmenhöhe"), or numerical values **embedded in graphics**. **Do not** ignore these "embedded annotations"

                -Treat **embedded numbers or text annotation** (e.g., tolerances like "–4 mm" or "max. +6 mm") as critical technical data, even if part of a graphic element.

                -Remember: small-font and embedded annotations (even if hard to read or non-horizontal) are critical technical data.

                Required Structured Output:

                    -**Component Names/Labels:** Identify all labeled parts (e.g., "Bürstenbrücke," "Flügelprofil").

                    -**Measurement Values with Contex**t: Specify what each measurement refers to (e.g., "Tolerance: ±2 mm for brush holder alignment").

                    -**Adjustment Steps**: Describe any illustrated procedures (e.g., "Rotate screw clockwise by 90° to adjust tension").

                    -Warnings/Cautions: Note symbols or text indicating risks (e.g., "Caution: Do not exceed +6 mm displacement").

                    -**Relative Positions**: Explicitly state spatial relationships (e.g., "Valve located at outer edge, left of centerline").

                Additional Rules:

                    -If the image shows adjustment ranges (e.g., angular limits) or rotation directions, describe them numerically and sequentially.

                    -**Never ignore** text or numbers**inside drawings**, even if they appear minor. Every annotation is intentional in technical schematics."

                    -**Visual Data:** Always **cross-reference textual content with the actual visual data** (image pixels, layout, arrows, component placements, labels, diagrams). Your summary **must remain objectively descriptive and rooted firmly in observable visual facts**.

                    - When reporting measurements or tolerances, always specify the **associated unit** (mm, Nm, etc.) and ensure the reported value matches the visual notation. If the unit is missing or ambiguous, flag this for review.

                    -**Confidence and Ambiguity Flagging**: If any label, measurement, or annotation is unclear, partially visible, or ambiguous, flag this in your report with a confidence note (e.g., 'Label partly obscured, may read as...').

            
            4. **Cross-Referencing Keys**C (Holistic Interpretation for the auxiliary product information)
                - In the process of understanding the  **product's structure, function, size and other details**, you need to always adhere to the folliwng guideline:
                    1. You must **not** treat any extracted key in isolation. Always **cross-reference** and synthesize all available extracted fields—especially **"product_component_information"**,** "embedded_table_chart"**, **"product_measurement_information"**, and **"side_margin_text"**. Consider how the information in one field provides context or clarifies data in the others. Describe, **where relevant**, **how the content of these keys interact, overlap, or complement each other** to form a complete, accurate understanding of the technical drawing and its purpose.
                    2. Analyze the interactions, dependencies, and overlaps between these fields, describing how they combine to provide a full technical picture.

            
                - Example for your dataset:

                    -When interpreting a dimension in an **"embedded_table_chart"**, check for corresponding annotations in **"product_measurement_information"** and further explanations in **"side_margin_text"*.

                    -If a part number or special instruction appears in both product_component_information and in the table, note this overlap and understand its purpose.

            #####
            5. **No Speculation:**
            	Do not speculate, infer, or hallucinate any information not explicitly supported by the textual or visual data.
            	Do not copy or repeat the extracted text verbatim; instead, synthesize it into a clear, comprehensive narrative.

            6.**Terminology & Integrity:**
               Always use the exact technical domain-specific terminology and part numbers as present in the original drawing and extracted fields. Do not paraphrase or translate technical identifiers
            	Always produce output in this clear JSON structure:

4. **Missing_OCR_result**
    After generating the **Image_summary (Comprehensive Narrative)**, perform a **completeness check:**
    - Carefully compare **every** number, label, and annotation present in the image pixels to those present in the given **`extracted_information`** fields. 
    - For every technical label, annotation, measurement, or component that is **visible** based on your reasoning ability in the image but **not** present in the **`extracted_information`** fields,  you **MUST**add a separate entry in **`"Missing_Product_information"`**:
        - `{"Small_Text_Body": "Text or label found visually in the image", "location": "introduce location or context"}`
    - If there are no missing items, output `"Missing_Product_information": []`
    - This section is **REQUIRED** and must always appear in the final JSON.
    
5.  **Metadata**
    Add important keywords which can used to fetch relevant document from vector store within our rag.
    1: check the technical drawings within the page
    2. The result should be a dictionary such as "topic_name : <topic_name_here>"
    3: Metadata should have the following format as dictionary
        - "topic_name : string" - Description: Best describing the topic of the page usually at the top or bottom of the page with bigger font
        - "technical_component_identifiers: Each identifier seperated with ',' as string with description " Example : "15-300-187-x BG stift für Band ,...."
        - "table_headers_columns" : Each name of table header column seperated with ',' as string " Example  : "Lauf/Führungswagen,Ohne,mit, ...."
        - "table_headers_rows" : Each name of table header rows seperated with ',' as string " Example  : "Anzahl Bänder,Bandstift (Bauselts), ...."
        - systems: Applicable systems
        - installation_positions: Where applicable (top, bottom, left, right)
        - glass_thickness: If glass specifications are mentioned
        - weight_specifications: Weight-related requirements
        - hardware_specs: Hardware and fastener specifications
        - additional_meta_data: See "Ocr_Result" key and add important keywords to metadata
    4: Important: Add metadata key as "N/A" if there is no value
"""