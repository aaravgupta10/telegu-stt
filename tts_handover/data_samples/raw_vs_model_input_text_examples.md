# Raw text vs the text the model receives (recorded examples)
Method: the raw string is taken verbatim from the SYSPIN Telugu male transcripts JSON; the 'after' string is the `transcript` field of the manifest written by prep_syspin.py in the local 4-clip test (file data_samples/local_prep_test_4clips_train.jsonl, produced 2026-10-18 ~09:50 IST). The model then receives these characters as SentencePiece ids from our tokenizer (the ids themselves were never printed: UNKNOWN - not found in records).

## A. Four clips: raw vs cleaned (recorded)
- id `IISc_SYSPINProject_te_m_OTHE_00519`
  - raw    : 'ముంబై వాంఖేడే స్టేడియంలో వెస్టీండీస్ తో సచిన్ చివరి మ్యాచ్ ఆడి రిటైర్మెంట్ ప్రకటించారు.'
  - cleaned: 'ముంబై వాంఖేడే స్టేడియంలో వెస్టీండీస్ తో సచిన్ చివరి మ్యాచ్ ఆడి రిటైర్మెంట్ ప్రకటించారు.'
  - identical after cleaning: True
- id `IISc_SYSPINProject_te_m_BOOK_04399`
  - raw    : 'చినుకులు కాలువలై, కాలువలు నదులై తాగునీరుగా సాగునీరుగా మారి మనిషికి ఆహరాన్ని, ఆరోగ్యాన్ని అందిస్తాయి.'
  - cleaned: 'చినుకులు కాలువలై, కాలువలు నదులై తాగునీరుగా సాగునీరుగా మారి మనిషికి ఆహరాన్ని, ఆరోగ్యాన్ని అందిస్తాయి.'
  - identical after cleaning: True
- id `IISc_SYSPINProject_te_m_WEAT_00331`
  - raw    : 'టాలీవుడ్లో కొత్త తారలతో, తక్కువ బడ్జెట్ తో భారీ విజయాలను అందుకొన్న నిర్మాత బెక్కెం వేణుగోపాల్ మేం వయసుకు వచ్చాం, ప్రేమ ఇష్క్ కాదల్ వంటి సినిమాలను చేశారు.'
  - cleaned: 'టాలీవుడ్లో కొత్త తారలతో, తక్కువ బడ్జెట్ తో భారీ విజయాలను అందుకొన్న నిర్మాత బెక్కెం వేణుగోపాల్ మేం వయసుకు వచ్చాం, ప్రేమ ఇష్క్ కాదల్ వంటి సినిమాలను చేశారు.'
  - identical after cleaning: True
- id `IISc_SYSPINProject_te_m_BOCU_03333`
  - raw    : ' సివిల్ సర్వీసు సిబ్బందికి సంబంధించిన క్రమశిక్షణా విషయాలపై కేంద్ర ప్రభుత్వానికి సలహాలిస్తుంది.'
  - cleaned: 'సివిల్ సర్వీసు సిబ్బందికి సంబంధించిన క్రమశిక్షణా విషయాలపై కేంద్ర ప్రభుత్వానికి సలహాలిస్తుంది.'
  - identical after cleaning: True

## B. What the text rules do to real raw transcripts (counts over the whole male transcripts JSON, 21,463 entries; examples verbatim)
- entries with a digit (ASCII or Telugu): 412  -> the clip is DROPPED (no number-to-words conversion exists in our pipeline). Cross-check: pilot stats.json reported 412 digit rejects (data_samples/pilot_prep_stats.json).
  - `IISc_SYSPINProject_te_m_BOOK_10045`: '{1786}{పదిహేడు వందల ఎనభై ఆరు}లో మన దేశానికి వచ్చి సంస్కృతం అభ్యసించిన సర్ విలియంజోన్స్ సంస్కృతానికీ, పర్షియన్, గ్రీక్, లాటిన్, కెల్టిక్, గోథిక్ తదితర యూరోపియన్ భాషలకూ ఉన్న పోలికలను గుర్తించాడు.'
  - `IISc_SYSPINProject_te_m_BOOK_16101`: '“శ్రీదేవీ, {12}{పన్నెండు} పిన్నులూ పెట్టేయి” అని ఉత్తర్వు జారీచేసి, తరవాత షాట్ తీయమని నృత్య దర్శకురాలు తారకు చెప్పి లొకేషన్ నుంచి వెళ్లిపోయారు.'
  - `IISc_SYSPINProject_te_m_BOCU_02642`: "{1984}{పంతొమ్మిది వందల ఎనభై నాలుగు} లో భారతదేశం 'ఐదు ఖండాలలోని ఆరు జాతి రాజ్యాల శాంతిచర్యల సమావేశాన్ని ప్రారంభించింది."
  - `IISc_SYSPINProject_te_m_BOOK_00784`: 'హార్వే మరణించిన {4}{నాలుగు} సంవత్సరాల తర్వాత {1661}{పదహారు వందల అరవై ఒకట}వ సంవత్సరంలో మాలఫ్ఫీజి గబ్బిలం రెక్కలపై అధ్యయనం చేశాడు.'
- entries with Latin letters: 0 -> DROPPED (character check)
- entries containing zero-width characters (removed by the cleaner, clip kept): 0
- entries with leading/trailing spaces (stripped): 1688

## C. Rasa Telugu raw rows (as printed by the owner; Rasa goes through the same cleaning code)
See data_samples/rasa_telugu_parquet_schema_and_two_rows.txt. Row 2 contains English words written in Telugu script (e.g. ఫ్యాకల్టీ, గవర్నమెంట్); such words stay as written. The cleaned versions of these two rows were not printed: UNKNOWN - not found in records.

## D. Observation from reading the raw male transcripts JSON (not acted on)
SYSPIN writes many numbers as a pair `{digits}{spoken Telugu form}`, e.g. `{1786}{పదిహేడు వందల ఎనభై ఆరు}`. Of the 412 entries our cleaner dropped because they contain digits, 412 contain such a pair, and 412 would contain no digit at all if only the spoken-form part were kept (0 would still contain digits). Whether the braces/pairs follow one convention in the female archive is UNKNOWN (not inspected). Our pipeline did not use this (those clips were dropped); it is recorded here because it is a possible way to recover the dropped clips and to teach numbers. Counts computed by reading the file; nothing was trained or generated.
