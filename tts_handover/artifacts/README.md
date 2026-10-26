# artifacts

`tokenizer.json`: the Telugu tokenizer of the full run (TRUN-0002), copied by the owner from the notebook `tts` (`~/SageMaker/tts/data/full/tokenizer.json`) and downloaded to the owner's PC on 2026-10-19 (file time 10:15 IST). 277,583 bytes, sha256 ee49d18766b06db26dc32a38658cac460b1deeeaaa67dd1bc57d14f1aaa304af. It was NOT in S3 or in the first version of this package; the provenance (notebook path) is the owner's statement, not independently verified, except that the file is consistent with the model: a Unigram tokenizer with exactly 4,000 entries (the model's `n_bins` is 4000).

Inspection (2026-10-19, read-only): model type Unigram; 4,000 vocabulary entries; unk id 0; normalizer = Prepend U+2581; pre-tokenizer = Metaspace; the five demo sentences encode with 0 unknown tokens and decode back correctly; about 0.29 tokens per character on the 20 digit-free test sentences (a 300-character sentence is about 86 tokens).

`tokenizer.model`: the SentencePiece source file of the same tokenizer, 92476 bytes, sha256 2078f2f43343d9f48f063c97004ceb79cd445d732fc55c852a0f4569d1b2c88a; copied by the owner and downloaded on 2026-10-19. Verified (read-only) to be the matching pair of `tokenizer.json`: both have 4,000 pieces (unk/bos/eos/pad ids 0/1/2/3) and give identical token ids on 25 Telugu sentences (5 demo examples and the 20 digit-free test sentences).

Not available: `tokenizer.vocab` of the full run (only on the notebook disk). The pilot tokenizer (a different file) was never copied off notebook `rag`. Backup of both files to S3: UNKNOWN.
