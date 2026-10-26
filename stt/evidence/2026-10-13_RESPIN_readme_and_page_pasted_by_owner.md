# RESPIN S1.0 corpus: README text and page screenshot, supplied by the owner, 2026-10-13

Source: the owner opened https://spiredatasets.ee.iisc.ac.in/respincorpus in their own browser and pasted the README text plus a screenshot of the page (the browser pane could not render the site). The README text below is reproduced as pasted. The screenshot showed the page title "RESPIN CORPUS" with tabs **Dataset Info, Download, Dataset Download info, Dataset Models Info**, a bar chart "Dev Set" (hours per language and dialect), and these "KEY FEATURES": 10k hours read-speech | 7.7M audio files | 197k sentences | 18.8k speakers from 1500+ pincodes | 9 Indian languages | 38 dialects | 2 domains (Agriculture & Finance). Citation requested: Saurabh et al., "RESPIN-S1.0: A read speech corpus of 10,000+ hours in dialects of nine Indian languages", 2025. Contents of the Download, Dataset Download info and Dataset Models Info tabs were NOT captured.

---

ReadMe

RESPIN S1.0 CORPUS
As a part of the RESPIN project, crowdsource read-speech data is being released. Audio and text files are made available to the public, promoting innovation in Automatic Speech Recognition for Indian languages.

Data Statistics
Type: Parallel Speech and Text
Language(s): Bengali (BN), Bhojpuri (BH), Chhattisgarhi (CH), Hindi (HI), Kannada (KN), Magahi (MG), Maithili (MT), Marathi (MR), Telugu (TE)
Linguality: Multilingual
Catalogue Id: RESPIN-S1.0
Total Audio Duration (HH:MM:SS): 9934:40:12
Average Sample Duration: 5.18 secs
Total Unique Text IDs: 197008
Recording Specifications: 16 kHz, 16 bits per sample, Mono
Recording Format: WAV
Recording Environment: Natural
Data creator: Indian Institute of Sciences (IISc), Bengaluru
Year of publishing: 2024
Suggested research purposes / areas: ASR, Language Identification, Dialect Identification, etc.

Dialect-Wise Summary (rows for Hindi and Telugu only; the paste also contained the other seven languages)
DID	#utt	#sent (Agri)	#sent (Bank)	#sent	#spk	#re-spk	Agri (hrs)	Bank (hrs)	Total (hrs)
train_hi_small	85800	8573	8587	17160	2172	1960	63.75	64.73	128.47
train_hi_clean	574544	9793	9690	19345	2305	2216	355.48	357.14	712.61
train_hi_seminoisy	181710	9702	9613	19180	2304	2220	134.31	138.96	273.27
train_hi_noisy	186275	9759	9665	19286	2314	2221	150.06	154.49	304.55
dev_hi	1539	388	334	722	100	100	1.17	1.03	2.21
train_te_small	95280	9528	9579	19056	1848	1415	77.17	78.72	155.89
train_te_clean	702883	10038	10035	19978	2287	1819	503.27	517.90	1021.16
train_te_seminoisy	111471	9704	9756	19370	2273	1819	91.33	94.77	186.10
train_te_noisy	73390	8995	9000	17914	2258	1747	63.19	64.47	127.66
dev_te	1438	265	235	500	80	80	1.21	1.09	2.30

Notes: DID: Dialect ID; #utt: Number of utterances; #sent: Number of sentences; #spk: Number of speakers; #re-spk: Number of reassigned speakers

Directory Structure
train_bn_small/
 D1/<speaker_id>/IISc_RESPIN_<lid>_<dialect>_<speaker_id>_<pincode>_<genderTag>_<domainTag>_<text_id>_<uttid>.wav
 (per-speaker .txt files), D2 ..., meta_train_bn_small.json, README.md

Metadata File Sample (meta_dev_bn.json): fields age_group, age_group_reassigned, dialect, domain, duration, gender, gender_reassigned, lid, pincode, slab (e.g. "clean"), speaker_id, speaker_id_reassigned, text, text_id, text_type ("statement"), utterance_id, wav_path. In the Bengali sample, English loanwords are written in Bengali script (e.g. "চিকেন হারভেস্টার মেশিনে পোল্ট্রি ফার্মের ...").

Copyright and license
ASR data created under RESPIN project by Indian Institute of Science, Bengaluru is available at http://spiredatasets.iisc.ac.in/respinCorpus and the copyright in the ASR data belongs to Indian Institute of Science, Bengaluru and the said ASR data is released or distributed under CC-BY-4.0 license (https://creativecommons.org/licenses/by/4.0/legalcode.en). The user of said ASR data is referred to the disclaimer of warranties section in the CC-BY-4.0 license agreement.

Acknowledgments
We extend our gratitude to all speakers from various districts whose contributions were fundamental to this initiative's success. We are particularly grateful to Navana Tech for their efforts in collecting and curating the ASR corpus. We thank the Bill and Melinda Gates Foundation for their generous support in this project.

Contact Information
SPIRE Lab, EE Dept., IISc, Bengaluru
Email: contact.respin@iisc.ac.in
