# Notebook terminal sessions, exactly as the owner pasted them into the Claude Code chat

Source: session transcript `~/.claude/projects/C--Users-Aarav-Gupta-Downloads-10X-STT/a74da6a2-c79a-486f-aedf-c65ae5bd666e.jsonl`, 46 user messages that contain notebook terminal text. Times are the transcript's UTC timestamps of the message (the owner pasted shortly after running). Redactions: host names (`ip-REDACTED`), the name of the Hugging Face token (`[HF-TOKEN-NAME-REDACTED]`); no token values appeared in the records. This is the closest thing to shell history that exists: the notebooks' own `~/.bash_history` was never copied to this machine (UNKNOWN - not found in records).

Notebook identities seen: `rag` (pilot; prompt host ip-...-23-240-12 and, later, a different host after restarts) and `tts` (full run; hosts ip-...-21-193-16 then ip-...-28-38-159 after a stop/start). The notebook name is not shown in the prompts; the mapping comes from the project log (TA-031, TA-019) and from GPU output (`nvidia-smi -L` showed 4 GPUs only on `tts`).


---

## Paste 01  (transcript user message #122, 2026-10-18T04:37:43.566Z)

```
[ec2-user@ip-REDACTED ~]$ df -h ~/SageMaker
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme2n1     40G   15G   24G  38% /home/ec2-user/SageMaker
[ec2-user@ip-REDACTED ~]$ echo hello | aws s3 cp - s3://aarav-10x/test.txt && aws s3 rm s3://aarav-10x/test.txt
delete: s3://aarav-10x/test.txt
[ec2-user@ip-REDACTED ~]$ curl -sI https://huggingface.co | head -1
HTTP/2 200 
[ec2-user@ip-REDACTED ~]$ mkdir -p ~/SageMaker/tts/scripts ~/SageMaker/tts/logs
[ec2-user@ip-REDACTED ~]$ source ~/.bashrc && which uv ffmpeg git
/usr/bin/which: no uv in (/home/ec2-user/.local/bin:/home/ec2-user/bin:/opt/amazon/openmpi/bin:/opt/amazon/efa/bin:/usr/local/cuda-13.2/bin:/usr/local/cuda-13.2/include:/usr/libexec/gcc/x86_64-amazon-linux/11:/opt/aws/bin:/home/ec2-user/anaconda3/bin:/home/ec2-user/anaconda3/condabin:/home/ec2-user/anaconda3/bin:/opt/amazon/openmpi/bin:/opt/amazon/efa/bin:/usr/share/Modules/bin:/usr/local/cuda-13.2/bin:/usr/local/cuda-13.2/include:/usr/libexec/gcc/x86_64-amazon-linux/11:/opt/aws/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin)
/usr/bin/which: no ffmpeg in (/home/ec2-user/.local/bin:/home/ec2-user/bin:/opt/amazon/openmpi/bin:/opt/amazon/efa/bin:/usr/local/cuda-13.2/bin:/usr/local/cuda-13.2/include:/usr/libexec/gcc/x86_64-amazon-linux/11:/opt/aws/bin:/home/ec2-user/anaconda3/bin:/home/ec2-user/anaconda3/condabin:/home/ec2-user/anaconda3/bin:/opt/amazon/openmpi/bin:/opt/amazon/efa/bin:/usr/share/Modules/bin:/usr/local/cuda-13.2/bin:/usr/local/cuda-13.2/include:/usr/libexec/gcc/x86_64-amazon-linux/11:/opt/aws/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin)
/usr/bin/git
(base) [ec2-user@ip-REDACTED ~]$ tail -25 ~/SageMaker/tts/logs/setup.log; ls ~/SageMaker ~/SageMaker/tts ~/SageMaker/bin
tail: cannot open '/home/ec2-user/SageMaker/tts/logs/setup.log' for reading: No such file or directory
ls: cannot access '/home/ec2-user/SageMaker/bin': No such file or directory
/home/ec2-user/SageMaker:
'JEE SFT Data Constitution & Generation Guidelines.pdf'  'paper1_q0378 (1).json'   paper1_q0648.json            paper2_q0151.json        paper2_q0437.json
'Untitled Folder'                                         paper1_q0378.json        paper1_q0649.json            paper2_q0152.json        paper2_q0438.json
 __pycache__                                             'paper1_q0379 (1).json'   paper1_q0650.json            paper2_q0153.json        paper2_q0439.json
 cache                                                    paper1_q0379.json        paper1_q0651.json            paper2_q0154.json        paper2_q0440.json
 check_template.py                                       'paper1_q0380 (1).json'   paper1_q0652.json            paper2_q0155.json       'paper2_q0441 (1).json'
 checkpoints                                              paper1_q0380.json        paper1_q0653.json            paper2_q0156.json        paper2_q0441.json
 classified.jsonl                                         paper1_q0381.json        paper1_q0654.json            paper2_q0157.json        paper2_q0442.json
 classify.cpython-311.pyc                                'paper1_q0382 (1).json'   paper1_q0655.json            paper2_q0158.json        paper2_q0443.json
 classify.py                                              paper1_q0382.json        paper1_q0656.json            paper2_q0159.json        paper2_q0444.json
 clean.jsonl                                             'paper1_q0383 (1).json'   paper1_q0657.json            paper2_q0160.json        paper2_q0445.json
 concept_pairs.cpython-311.pyc                            paper1_q0383.json        paper1_q0658.json            paper2_q0161.json        paper2_q0446.json
 concept_pairs.py                                        'paper1_q0384 (1).json'   paper1_q0659.json            paper2_q0162.json        paper2_q0447.json
 data                                                     paper1_q0384.json        paper1_q0660.json            paper2_q0163.json        paper2_q0448.json
 decontaminate.log                                        paper1_q0385.json        paper1_q0661.json            paper2_q0164.json        paper2_q0449.json
 decontaminate.py                                         paper1_q0386.json        paper1_q0662.json            paper2_q0165.json       'paper2_q0450 (1).json'
 decontamination_dropped.jsonl                            paper1_q0387.json        paper1_q0663.json            paper2_q0166.json        paper2_q0450.json
 dropped_figure_converted.jsonl                           paper1_q0388.json        paper1_q0664.json            paper2_q0167.json       'paper2_q0451 (1).json'
 eval                                                     paper1_q0389.json        paper1_q0665.json            paper2_q0168.json        paper2_q0451.json
 evaluate.py                                             'paper1_q0390 (1).json'   paper1_q0666.json            paper2_q0169.json        paper2_q0452.json
 extract.cpython-311.pyc                                  paper1_q0390.json        paper1_q0667.json            paper2_q0170.json       'paper2_q0453 (1).json'
 extract.log                                              paper1_q0391.json        paper1_q0668.json            paper2_q0171.json        paper2_q0453.json
 extract.py                                               paper1_q0392.json        paper1_q0669.json            paper2_q0172.json        paper2_q0454.json
 extracted.jsonl                                          paper1_q0393.json        paper1_q0670.json            paper2_q0173.json        paper2_q0455.json
 extraction_raw                                           paper1_q0394.json        paper1_q0671.json            paper2_q0174.json       'paper2_q0456 (1).json'
 generate.log                                             paper1_q0395.json        paper1_q0672.json           'paper2_q0175 (1).json'   paper2_q0456.json
 generate.py                                              paper1_q0396.json        paper1_q0673.json            paper2_q0175.json       'paper2_q0457 (1).json'
 generate_inference.jsonl                                 paper1_q0397.json       'paper1_q0674 (1).json'       paper2_q0176.json        paper2_q0457.json
 inference.jsonl                                          paper1_q0398.json        paper1_q0674.json            paper2_q0177.json        paper2_q0458.json
 input                                                    paper1_q0399.json       'paper1_q0675 (1).json'       paper2_q0178.json        paper2_q0459.json
 integrity.cpython-311.pyc                                paper1_q0400.json        paper1_q0675.json            paper2_q0179.json        paper2_q0460.json
 integrity.py                                             paper1_q0401.json        paper1_q0676.json            paper2_q0180.json        paper2_q0461.json
 integrity_clean_uids.json                                paper1_q0402.json       'paper1_q0677 (1).json'       paper2_q0181.json       'paper2_q0462 (1).json'
 intra_pool_duplicates.jsonl                              paper1_q0403.json        paper1_q0677.json            paper2_q0182.json        paper2_q0462.json
 jee_sft                                                  paper1_q0404.json        paper1_q0678.json            paper2_q0183.json        paper2_q0463.json
 latex_numbers.cpython-311.pyc                            paper1_q0405.json       'paper1_q0679 (1).json'       paper2_q0184.json        paper2_q0464.json
 latex_numbers.py                                         paper1_q0406.json        paper1_q0679.json            paper2_q0185.json       'paper2_q0465 (1).json'
 lost+found                                               paper1_q0407.json       'paper1_q0680 (1).json'       paper2_q0186.json        paper2_q0465.json
 low_confidence.jsonl                                     paper1_q0408.json        paper1_q0680.json            paper2_q0187.json        paper2_q0466.json
 merge.py                                                 paper1_q0409.json        paper1_q0681.json            paper2_q0188.json        paper2_q0467.json
'page_0010 (1).png'                                       paper1_q0410.json        paper1_q0682.json            paper2_q0189.json        paper2_q0468.json
 page_0010.png                                            paper1_q0411.json        paper1_q0683.json            paper2_q0190.json        paper2_q0469.json
 page_0019.png                                            paper1_q0412.json        paper1_q0684.json            paper2_q0191.json        paper2_q0470.json
 page_0020.png                                            paper1_q0413.json        paper1_q0685.json            paper2_q0192.json        paper2_q0471.json
 page_0022.png                                            paper1_q0414.json        paper1_q0686.json            paper2_q0193.json        paper2_q0472.json
 page_0024.png                                            paper1_q0415.json        paper1_q0687.json            paper2_q0194.json        paper2_q0473.json
'page_0026 (1).png'                                       paper1_q0416.json        paper1_q0688.json            paper2_q0195.json        paper2_q0474.json
'page_0037 (1).png'                                       paper1_q0417.json        paper1_q0689.json            paper2_q0196.json        paper2_q0475.json
'page_0051 (1).png'                                       paper1_q0418.json       'paper1_q0690 (1).json'       paper2_q0197.json        paper2_q0476.json
'page_0054 (1).png'                                       paper1_q0419.json        paper1_q0690.json            paper2_q0198.json        paper2_q0477.json
 page_0061.png                                            paper1_q0420.json        paper1_q0691.json            paper2_q0199.json        paper2_q0478.json
'page_0062 (1).png'                                       paper1_q0421.json        paper1_q0692.json            paper2_q0200.json       'paper2_q0479 (1).json'
 page_0072.png                                            paper1_q0422.json        paper1_q0693.json            paper2_q0201.json        paper2_q0479.json
 page_0081.png                                            paper1_q0423.json        paper1_q0694.json            paper2_q0202.json       'paper2_q0480 (1).json'
 page_0083.png                                            paper1_q0424.json        paper1_q0695.json            paper2_q0203.json        paper2_q0480.json
 page_0085.png                                            paper1_q0425.json        paper1_q0696.json            paper2_q0204.json       'paper2_q0481 (1).json'
'page_0087 (1).png'                                      'paper1_q0426 (1).json'   paper1_q0697.json            paper2_q0205.json        paper2_q0481.json
 page_0087.png                                            paper1_q0426.json        paper1_q0698.json           'paper2_q0206 (1).json'   paper2_q0482.json
'page_0101 (1).png'                                       paper1_q0427.json       'paper1_q0699 (1).json'       paper2_q0206.json        paper2_q0483.json
'page_0114 (1).png'                                       paper1_q0428.json        paper1_q0699.json            paper2_q0207.json        paper2_q0484.json
 page_0129.png                                           'paper1_q0429 (1).json'   paper1_q0700.json            paper2_q0208.json        paper2_q0485.json
'page_0130 (1).png'                                       paper1_q0429.json       'paper1_q0701 (1).json'       paper2_q0209.json        paper2_q0486.json
'page_0133 (1).png'                                      'paper1_q0430 (1).json'   paper1_q0701.json            paper2_q0210.json        paper2_q0487.json
 page_0139.png                                            paper1_q0430.json        paper1_q0702.json            paper2_q0211.json        paper2_q0488.json
'page_0140 (1).png'                                       paper1_q0431.json       'paper1_q0703 (1).json'       paper2_q0212.json        paper2_q0489.json
 page_0141.png                                            paper1_q0432.json        paper1_q0703.json            paper2_q0213.json        paper2_q0490.json
 page_0143.png                                            paper1_q0433.json        paper1_q0704.json            paper2_q0214.json        paper2_q0491.json
 page_0145.png                                            paper1_q0434.json        paper1_q0705.json            paper2_q0215.json        paper2_q0492.json
 page_0146.png                                            paper1_q0435.json        paper1_q0706.json            paper2_q0216.json        paper2_q0493.json
'page_0164 (1).png'                                       paper1_q0436.json        paper1_q0707.json            paper2_q0217.json        paper2_q0494.json
'page_0175 (1).png'                                       paper1_q0437.json        paper1_q0708.json            paper2_q0218.json        paper2_q0495.json
'page_0185 (1).png'                                       paper1_q0438.json        paper1_q0709.json            paper2_q0219.json        paper2_q0496.json
 page_0193.png                                            paper1_q0439.json        paper1_q0710.json            paper2_q0220.json        paper2_q0497.json
'page_0196 (1).png'                                       paper1_q0440.json        paper1_q0711.json            paper2_q0221.json        paper2_q0498.json
'page_0198 (1).png'                                       paper1_q0441.json        paper1_q0712.json            paper2_q0222.json        paper2_q0499.json
 page_0201.png                                            paper1_q0442.json        paper1_q0713.json            paper2_q0223.json        paper2_q0500.json
 page_0207.png                                            paper1_q0443.json        paper1_q0714.json            paper2_q0224.json        paper2_q0501.json
 page_0209.png                                            paper1_q0444.json        paper1_q0715.json            paper2_q0225.json       'paper2_q0502 (1).json'
 page_0210.png                                            paper1_q0445.json        paper1_q0716.json           'paper2_q0226 (1).json'   paper2_q0502.json
 page_0211.png                                           'paper1_q0446 (1).json'   paper1_q0717.json            paper2_q0226.json        paper2_q0503.json
'page_0214 (1).png'                                       paper1_q0446.json        paper1_q0718.json            paper2_q0227.json       'paper2_q0504 (1).json'
'page_0222 (1).png'                                       paper1_q0447.json        paper1_q0719.json           'paper2_q0228 (1).json'   paper2_q0504.json
'page_0223 (1).png'                                       paper1_q0448.json        paper1_q0720.json            paper2_q0228.json       'paper2_q0505 (1).json'
'page_0224 (1).png'                                       paper1_q0449.json        paper1_q0721.json            paper2_q0229.json        paper2_q0505.json
'page_0225 (1).png'                                       paper1_q0450.json        paper1_q0722.json            paper2_q0230.json        paper2_q0506.json
'page_0226 (1).png'                                       paper1_q0451.json        paper1_q0723.json            paper2_q0231.json        paper2_q0507.json
'page_0227 (1).png'                                       paper1_q0452.json        paper1_q0724.json            paper2_q0232.json        paper2_q0508.json
'page_0228 (1).png'                                       paper1_q0453.json        paper1_q0725.json            paper2_q0233.json        paper2_q0509.json
'page_0229 (1).png'                                       paper1_q0454.json       'paper1_q0726 (1).json'       paper2_q0234.json        paper2_q0510.json
'page_0230 (1).png'                                       paper1_q0455.json        paper1_q0726.json            paper2_q0235.json        paper2_q0511.json
'page_0231 (1).png'                                       paper1_q0456.json        paper1_q0727.json            paper2_q0236.json        paper2_q0512.json
'page_0232 (1).png'                                       paper1_q0457.json        paper1_q0728.json            paper2_q0237.json        paper2_q0513.json
'page_0233 (1).png'                                       paper1_q0458.json        paper1_q0730.json           'paper2_q0238 (1).json'   paper2_q0514.json
'page_0244 (1).png'                                      'paper1_q0459 (1).json'   paper1_q0731.json            paper2_q0238.json        paper2_q0515.json
 page_0257.png                                            paper1_q0459.json        paper1_q0732.json            paper2_q0239.json        paper2_q0516.json
'page_0259 (1).png'                                       paper1_q0460.json        paper1_q0733.json           'paper2_q0240 (1).json'   paper2_q0517.json
'page_0266 (1).png'                                       paper1_q0461.json        paper1_q0734.json            paper2_q0240.json        paper2_q0518.json
 page_0267.png                                            paper1_q0462.json        paper1_q0735.json            paper2_q0241.json        paper2_q0519.json
'page_0272 (1).png'                                       paper1_q0463.json        paper1_q0736.json           'paper2_q0242 (1).json'   paper2_q0520.json
 page_0272.png                                            paper1_q0464.json       'paper1_q0737 (1).json'       paper2_q0242.json        paper2_q0521.json
'page_0273 (1).png'                                       paper1_q0465.json        paper1_q0737.json            paper2_q0243.json        paper2_q0522.json
 page_0274.png                                            paper1_q0466.json        paper1_q0738.json            paper2_q0244.json        paper2_q0523.json
 page_0276.png                                            paper1_q0467.json        paper1_q0739.json            paper2_q0245.json        paper2_q0524.json
 page_0277.png                                            paper1_q0468.json        paper1_q0740.json            paper2_q0247.json        paper2_q0525.json
'page_0298 (1).png'                                       paper1_q0469.json        paper1_q0741.json            paper2_q0248.json        paper2_q0526.json
'page_0299 (1).png'                                       paper1_q0470.json        paper1_q0742.json            paper2_q0249.json       'paper2_q0527 (1).json'
'page_0300 (1).png'                                       paper1_q0471.json        paper1_q0743.json            paper2_q0250.json        paper2_q0527.json
'page_0301 (1).png'                                       paper1_q0472.json        paper1_q0744.json            paper2_q0251.json        paper2_q0528.json
'page_0302 (1).png'                                       paper1_q0475.json        paper1_q0745.json            paper2_q0252.json        paper2_q0529.json
'page_0303 (1).png'                                       paper1_q0476.json        paper1_q0746.json            paper2_q0253.json        paper2_q0530.json
'page_0304 (1).png'                                       paper1_q0477.json        paper1_q0747.json            paper2_q0254.json        paper2_q0531.json
'page_0305 (1).png'                                       paper1_q0478.json        paper1_q0748.json            paper2_q0255.json        paper2_q0532.json
'page_0309 (1).png'                                       paper1_q0479.json       'paper1_q0749 (1).json'       paper2_q0256.json        paper2_q0533.json
'page_0312 (1).png'                                       paper1_q0480.json        paper1_q0749.json            paper2_q0257.json        paper2_q0534.json
'page_0316 (1).png'                                       paper1_q0481.json        paper1_q0750.json            paper2_q0258.json        paper2_q0535.json
'page_0317 (1).png'                                       paper1_q0482.json        paper1_q0751.json            paper2_q0259.json        paper2_q0536.json
'page_0333 (1).png'                                       paper1_q0483.json        paper1_q0752.json            paper2_q0260.json        paper2_q0537.json
 page_0338.png                                            paper1_q0484.json       'paper1_q0753 (1).json'       paper2_q0261.json        paper2_q0538.json
'page_0340 (1).png'                                       paper1_q0485.json        paper1_q0753.json            paper2_q0262.json        paper2_q0539.json
 page_0342.png                                            paper1_q0486.json        paper1_q0754.json            paper2_q0263.json        paper2_q0540.json
 page_0346.png                                            paper1_q0487.json        paper1_q0755.json            paper2_q0264.json       'paper2_q0541 (1).json'
 page_0348.png                                            paper1_q0488.json        paper1_q0756.json            paper2_q0265.json        paper2_q0541.json
 page_0349.png                                            paper1_q0489.json        paper1_q0757.json            paper2_q0266.json        paper2_q0542.json
 page_0352.png                                            paper1_q0490.json        paper1_q0758.json            paper2_q0267.json        paper2_q0543.json
'page_0356 (1).png'                                      'paper1_q0491 (1).json'   paper1_q0759.json            paper2_q0268.json        paper2_q0544.json
'page_0358 (1).png'                                       paper1_q0491.json        paper1_q0760.json            paper2_q0269.json        paper2_q0545.json
'page_0359 (1).png'                                       paper1_q0492.json        paper1_q0761.json            paper2_q0270.json        paper2_q0546.json
'page_0360 (1).png'                                       paper1_q0493.json        paper1_q0762.json            paper2_q0271.json        paper2_q0547.json
'page_0381 (1).png'                                       paper1_q0494.json        paper1_q0763.json            paper2_q0272.json        paper2_q0548.json
'page_0409 (1).png'                                       paper1_q0495.json        paper1_q0764.json            paper2_q0273.json        paper2_q0549.json
'page_0410 (1).png'                                       paper1_q0496.json        paper1_q0765.json            paper2_q0274.json        paper2_q0550.json
'page_0414 (1).png'                                       paper1_q0497.json        paper1_q0766.json            paper2_q0275.json        paper2_q0551.json
'page_0417 (1).png'                                       paper1_q0498.json        paper1_q0767.json            paper2_q0276.json        paper2_q0552.json
 page_0420.png                                            paper1_q0499.json       'paper1_q0768 (1).json'       paper2_q0277.json        paper2_q0553.json
 page_0429.png                                            paper1_q0500.json        paper1_q0768.json            paper2_q0278.json        paper2_q0554.json
'page_0434 (1).png'                                       paper1_q0501.json       'paper1_q0769 (1).json'       paper2_q0279.json        paper2_q0555.json
 page_0435.png                                            paper1_q0502.json        paper1_q0769.json            paper2_q0280.json        paper2_q0556.json
 page_0436.png                                            paper1_q0503.json        paper1_q0770.json           'paper2_q0281 (1).json'   paper2_q0557.json
 page_0438.png                                            paper1_q0504.json        paper1_q0771.json            paper2_q0281.json        paper2_q0558.json
 page_0440.png                                            paper1_q0506.json        paper1_q0772.json            paper2_q0282.json        paper2_q0559.json
'page_0455 (1).png'                                       paper1_q0507.json        paper1_q0773.json            paper2_q0283.json        paper2_q0560.json
'page_0457 (1).png'                                       paper1_q0508.json        paper1_q0774.json            paper2_q0284.json        paper2_q0561.json
'page_0458 (1).png'                                       paper1_q0509.json        paper1_q0775.json            paper2_q0285.json        paper2_q0562.json
'page_0461 (1).png'                                       paper1_q0510.json        paper1_q0776.json           'paper2_q0286 (1).json'   paper2_q0563.json
 page_0487.png                                            paper1_q0511.json        paper1_q0777.json            paper2_q0286.json        paper2_q0564.json
'page_0488 (1).png'                                       paper1_q0512.json        paper1_q0778.json           'paper2_q0287 (1).json'   paper2_q0565.json
 page_0494.png                                            paper1_q0513.json        paper2                       paper2_q0287.json        paper2_q0566.json
 page_0497.png                                           'paper1_q0514 (1).json'   paper2_p0001_fallback.json   paper2_q0288.json        paper2_q0567.json
'page_0498 (1).png'                                       paper1_q0514.json        paper2_p0002_fallback.json  'paper2_q0289 (1).json'   paper2_q0568.json
 page_0499.png                                           'paper1_q0515 (1).json'   paper2_p0003_fallback.json   paper2_q0289.json        paper2_q0569.json
 page_0500.png                                            paper1_q0515.json        paper2_q0001.json            paper2_q0290.json        paper2_q0570.json
 page_0502.png                                            paper1_q0516.json        paper2_q0002.json            paper2_q0291.json        paper2_q0571.json
'page_0505 (1).png'                                       paper1_q0517.json        paper2_q0003.json            paper2_q0292.json        paper2_q0572.json
'page_0506 (1).png'                                       paper1_q0518.json        paper2_q0004.json            paper2_q0293.json        paper2_q0573.json
'page_0507 (1).png'                                       paper1_q0519.json        paper2_q0005.json            paper2_q0294.json        paper2_q0574.json
'page_0508 (1).png'                                       paper1_q0520.json        paper2_q0006.json            paper2_q0295.json        paper2_q0576.json
'page_0541 (1).png'                                      'paper1_q0521 (1).json'   paper2_q0007.json            paper2_q0296.json        paper2_q0577.json
'page_0542 (1).png'                                       paper1_q0521.json        paper2_q0008.json            paper2_q0297.json        paper2_q0578.json
 page_0550.png                                           'paper1_q0522 (1).json'   paper2_q0009.json            paper2_q0298.json        paper2_q0579.json
'page_0551 (1).png'                                       paper1_q0522.json        paper2_q0010.json            paper2_q0299.json        paper2_q0580.json
'page_0554 (1).png'                                       paper1_q0523.json        paper2_q0011.json           'paper2_q0300 (1).json'   paper2_q0581.json
'page_0555 (1).png'                                       paper1_q0524.json        paper2_q0012.json            paper2_q0300.json        paper2_q0582.json
 page_0555.png                                           'paper1_q0525 (1).json'  'paper2_q0013 (1).json'       paper2_q0301.json        paper2_q0583.json
'page_0557 (1).png'                                       paper1_q0525.json        paper2_q0013.json            paper2_q0302.json        paper2_q0584.json
 page_0558.png                                            paper1_q0526.json        paper2_q0014.json            paper2_q0303.json        paper2_q0585.json
 page_0559.png                                            paper1_q0527.json        paper2_q0015.json            paper2_q0304.json       'paper2_q0586 (1).json'
 page_0560.png                                            paper1_q0528.json       'paper2_q0016 (1).json'       paper2_q0305.json        paper2_q0586.json
 page_0562.png                                           'paper1_q0529 (1).json'   paper2_q0016.json            paper2_q0306.json        paper2_q0587.json
 page_0592.png                                            paper1_q0529.json        paper2_q0017.json            paper2_q0307.json        paper2_q0588.json
 paper1                                                   paper1_q0530.json        paper2_q0018.json            paper2_q0308.json        paper2_q0589.json
 paper1_q0008.json                                       'paper1_q0531 (1).json'   paper2_q0019.json            paper2_q0309.json        paper2_q0590.json
 paper1_q0009.json                                        paper1_q0531.json        paper2_q0020.json            paper2_q0310.json        paper2_q0591.json
 paper1_q0016.json                                       'paper1_q0532 (1).json'   paper2_q0021.json            paper2_q0311.json        paper2_q0592.json
 paper1_q0020.json                                        paper1_q0532.json        paper2_q0022.json            paper2_q0312.json       'paper2_q0593 (1).json'
 paper1_q0028.json                                        paper1_q0533.json        paper2_q0023.json            paper2_q0313.json        paper2_q0593.json
 paper1_q0050.json                                        paper1_q0534.json        paper2_q0024.json            paper2_q0314.json        paper2_q0594.json
 paper1_q0052.json                                       'paper1_q0535 (1).json'   paper2_q0025.json            paper2_q0315.json        paper2_q0595.json
 paper1_q0058.json                                        paper1_q0535.json        paper2_q0026.json            paper2_q0316.json        paper2_q0596.json
 paper1_q0061.json                                        paper1_q0536.json        paper2_q0027.json            paper2_q0317.json        paper2_q0597.json
 paper1_q0063.json                                        paper1_q0537.json        paper2_q0028.json            paper2_q0318.json        paper2_q0598.json
 paper1_q0069.json                                        paper1_q0538.json       'paper2_q0029 (1).json'       paper2_q0319.json        paper2_q0599.json
 paper1_q0074.json                                       'paper1_q0539 (1).json'   paper2_q0029.json            paper2_q0320.json        paper2_q0600.json
 paper1_q0075.json                                        paper1_q0539.json        paper2_q0030.json            paper2_q0321.json        paper2_q0601.json
 paper1_q0080.json                                       'paper1_q0540 (1).json'   paper2_q0031.json            paper2_q0322.json        paper2_q0602.json
 paper1_q0081.json                                        paper1_q0540.json        paper2_q0032.json            paper2_q0323.json        paper2_q0603.json
 paper1_q0082.json                                        paper1_q0541.json       'paper2_q0033 (1).json'       paper2_q0324.json        paper2_q0604.json
 paper1_q0090.json                                        paper1_q0542.json        paper2_q0033.json            paper2_q0325.json        paper2_q0605.json
 paper1_q0095.json                                       'paper1_q0543 (1).json'   paper2_q0034.json            paper2_q0326.json        paper2_q0606.json
 paper1_q0118.json                                        paper1_q0543.json        paper2_q0035.json            paper2_q0327.json        paper2_q0607.json
 paper1_q0123.json                                        paper1_q0544.json        paper2_q0036.json            paper2_q0328.json        paper2_q0608.json
'paper1_q0129 (1).json'                                   paper1_q0545.json        paper2_q0037.json            paper2_q0329.json       'paper2_q0609 (1).json'
 paper1_q0129.json                                        paper1_q0546.json        paper2_q0038.json            paper2_q0330.json        paper2_q0609.json
 paper1_q0130.json                                        paper1_q0547.json        paper2_q0039.json            paper2_q0331.json        paper2_q0610.json
 paper1_q0136.json                                       'paper1_q0548 (1).json'   paper2_q0040.json           'paper2_q0332 (1).json'   paper2_q0611.json
 paper1_q0139.json                                        paper1_q0548.json        paper2_q0041.json            paper2_q0332.json        paper2_q0612.json
 paper1_q0142.json                                       'paper1_q0549 (1).json'   paper2_q0042.json            paper2_q0333.json        paper2_q0613.json
 paper1_q0146.json                                        paper1_q0549.json        paper2_q0043.json            paper2_q0334.json        paper2_q0614.json
 paper1_q0147.json                                        paper1_q0550.json        paper2_q0044.json           'paper2_q0335 (1).json'   paper2_q0615.json
 paper1_q0148.json                                        paper1_q0551.json        paper2_q0045.json            paper2_q0335.json        paper2_q0616.json
 paper1_q0149.json                                        paper1_q0552.json        paper2_q0046.json            paper2_q0336.json       'paper2_q0617 (1).json'
 paper1_q0154.json                                        paper1_q0553.json        paper2_q0047.json            paper2_q0337.json        paper2_q0617.json
 paper1_q0165.json                                        paper1_q0554.json        paper2_q0048.json            paper2_q0338.json       'paper2_q0618 (1).json'
 paper1_q0178.json                                        paper1_q0555.json        paper2_q0049.json            paper2_q0339.json        paper2_q0618.json
 paper1_q0207.json                                        paper1_q0556.json        paper2_q0050.json            paper2_q0340.json        paper2_q0619.json
 paper1_q0211.json                                        paper1_q0557.json        paper2_q0051.json            paper2_q0341.json        paper2_q0620.json
 paper1_q0212.json                                        paper1_q0558.json        paper2_q0052.json            paper2_q0342.json        paper2_q0621.json
 paper1_q0220.json                                        paper1_q0559.json        paper2_q0053.json            paper2_q0343.json        paper2_q0622.json
 paper1_q0225.json                                        paper1_q0560.json        paper2_q0054.json            paper2_q0344.json        paper2_q0623.json
 paper1_q0242.json                                        paper1_q0561.json        paper2_q0055.json            paper2_q0345.json        paper2_q0624.json
 paper1_q0262.json                                        paper1_q0562.json        paper2_q0056.json            paper2_q0346.json        paper2_q0625.json
 paper1_q0286.json                                        paper1_q0563.json        paper2_q0057.json            paper2_q0347.json       'paper2_q0626 (1).json'
 paper1_q0287.json                                        paper1_q0564.json        paper2_q0058.json            paper2_q0348.json        paper2_q0626.json
 paper1_q0297.json                                        paper1_q0565.json        paper2_q0059.json            paper2_q0349.json        paper2_q0627.json
'paper1_q0301 (1).json'                                   paper1_q0566.json        paper2_q0060.json            paper2_q0350.json        paper2_q0628.json
 paper1_q0301.json                                        paper1_q0567.json        paper2_q0061.json            paper2_q0351.json        paper2_q0629.json
 paper1_q0302.json                                        paper1_q0568.json        paper2_q0062.json            paper2_q0352.json        paper2_q0630.json
 paper1_q0303.json                                        paper1_q0569.json        paper2_q0063.json           'paper2_q0353 (1).json'   paper2_q0631.json
'paper1_q0305 (1).json'                                   paper1_q0570.json        paper2_q0064.json            paper2_q0353.json        paper2_q0632.json
 paper1_q0305.json                                        paper1_q0571.json        paper2_q0065.json            paper2_q0354.json        paper2_q0633.json
'paper1_q0306 (1).json'                                   paper1_q0572.json        paper2_q0066.json            paper2_q0355.json        paper2_q0634.json
 paper1_q0306.json                                        paper1_q0573.json        paper2_q0067.json           'paper2_q0356 (1).json'   paper2_q0635.json
 paper1_q0307.json                                        paper1_q0574.json        paper2_q0068.json            paper2_q0356.json        paper2_q0636.json
 paper1_q0308.json                                        paper1_q0575.json        paper2_q0069.json            paper2_q0357.json        paper2_q0637.json
 paper1_q0309.json                                       'paper1_q0576 (1).json'   paper2_q0070.json            paper2_q0358.json        paper2_q0638.json
 paper1_q0310.json                                        paper1_q0576.json        paper2_q0071.json            paper2_q0359.json        paper2_q0639.json
 paper1_q0311.json                                        paper1_q0577.json        paper2_q0072.json            paper2_q0360.json        paper2_q0640.json
 paper1_q0312.json                                        paper1_q0578.json        paper2_q0073.json           'paper2_q0361 (1).json'   paper2_q0641.json
'paper1_q0313 (1).json'                                   paper1_q0579.json        paper2_q0074.json            paper2_q0361.json        paper2_q0642.json
 paper1_q0313.json                                        paper1_q0580.json        paper2_q0075.json            paper2_q0362.json        paper2_q0643.json
 paper1_q0314.json                                        paper1_q0581.json        paper2_q0076.json            paper2_q0363.json        paper2_q0644.json
 paper1_q0315.json                                        paper1_q0582.json        paper2_q0077.json            paper2_q0364.json        paper2_q0645.json
 paper1_q0316.json                                        paper1_q0583.json        paper2_q0078.json            paper2_q0365.json        paper2_q0646.json
 paper1_q0317.json                                        paper1_q0584.json        paper2_q0079.json            paper2_q0366.json        paper2_q0647.json
 paper1_q0318.json                                        paper1_q0585.json        paper2_q0080.json            paper2_q0367.json        paper2_q0648.json
 paper1_q0319.json                                        paper1_q0586.json        paper2_q0081.json            paper2_q0368.json        paper2_q0649.json
 paper1_q0320.json                                        paper1_q0587.json        paper2_q0082.json            paper2_q0369.json        paper2_q0650.json
 paper1_q0321.json                                        paper1_q0588.json        paper2_q0083.json            paper2_q0370.json        paper2_q0652.json
 paper1_q0322.json                                        paper1_q0589.json        paper2_q0084.json            paper2_q0371.json        paper2_q0653.json
 paper1_q0323.json                                        paper1_q0590.json        paper2_q0085.json            paper2_q0372.json        paper2_q0654.json
 paper1_q0324.json                                        paper1_q0591.json        paper2_q0086.json            paper2_q0373.json        paper2_q0655.json
 paper1_q0325.json                                        paper1_q0592.json        paper2_q0087.json            paper2_q0374.json        paper2_q0656.json
 paper1_q0326.json                                        paper1_q0593.json        paper2_q0088.json           'paper2_q0375 (1).json'   paper2_q0657.json
 paper1_q0327.json                                        paper1_q0594.json        paper2_q0089.json            paper2_q0375.json        paper2_q0658.json
 paper1_q0328.json                                        paper1_q0595.json        paper2_q0090.json            paper2_q0376.json        paper2_q0659.json
 paper1_q0329.json                                        paper1_q0596.json        paper2_q0091.json            paper2_q0377.json        paper2_q0660.json
 paper1_q0330.json                                        paper1_q0597.json        paper2_q0092.json            paper2_q0378.json        paper2_q0661.json
 paper1_q0331.json                                        paper1_q0598.json        paper2_q0093.json            paper2_q0379.json        paper2_q0662.json
 paper1_q0332.json                                        paper1_q0599.json        paper2_q0094.json            paper2_q0380.json        paper2_q0663.json
 paper1_q0333.json                                       'paper1_q0600 (1).json'   paper2_q0095.json           'paper2_q0381 (1).json'  'paper2_q0664 (1).json'
 paper1_q0334.json                                        paper1_q0600.json        paper2_q0096.json            paper2_q0381.json        paper2_q0664.json
 paper1_q0335.json                                       'paper1_q0601 (1).json'   paper2_q0097.json            paper2_q0382.json        paper2_q0665.json
 paper1_q0336.json                                        paper1_q0601.json       'paper2_q0098 (1).json'       paper2_q0383.json        paper2_q0666.json
 paper1_q0337.json                                        paper1_q0602.json        paper2_q0098.json            paper2_q0384.json        paper2_q0667.json
 paper1_q0338.json                                       'paper1_q0603 (1).json'   paper2_q0099.json            paper2_q0385.json        paper2_q0668.json
 paper1_q0339.json                                        paper1_q0603.json        paper2_q0100.json            paper2_q0386.json        paper2_q0669.json
 paper1_q0340.json                                       'paper1_q0604 (1).json'   paper2_q0101.json            paper2_q0387.json        paper2_q0670.json
'paper1_q0341 (1).json'                                   paper1_q0604.json        paper2_q0102.json            paper2_q0388.json        paper2_q0671.json
 paper1_q0341.json                                       'paper1_q0605 (1).json'   paper2_q0103.json           'paper2_q0389 (1).json'   paper2_q0672.json
 paper1_q0342.json                                        paper1_q0605.json        paper2_q0104.json            paper2_q0389.json        paper2_q0673.json
 paper1_q0343.json                                       'paper1_q0606 (1).json'   paper2_q0105.json            paper2_q0390.json       'paper2_q0674 (1).json'
 paper1_q0344.json                                        paper1_q0606.json        paper2_q0106.json            paper2_q0391.json        paper2_q0674.json
 paper1_q0345.json                                        paper1_q0607.json       'paper2_q0107 (1).json'       paper2_q0393.json        paper2_q0675.json
 paper1_q0346.json                                        paper1_q0608.json        paper2_q0107.json            paper2_q0394.json        paper2_q0676.json
 paper1_q0347.json                                       'paper1_q0609 (1).json'   paper2_q0108.json            paper2_q0395.json       'paper2_q0677 (1).json'
 paper1_q0348.json                                        paper1_q0609.json        paper2_q0109.json            paper2_q0396.json        paper2_q0677.json
 paper1_q0349.json                                        paper1_q0610.json        paper2_q0110.json            paper2_q0397.json        paper2_q0678.json
 paper1_q0350.json                                        paper1_q0611.json        paper2_q0111.json            paper2_q0398.json        paper2_q0679.json
 paper1_q0351.json                                        paper1_q0612.json        paper2_q0112.json            paper2_q0399.json        paper2_q0680.json
 paper1_q0352.json                                        paper1_q0613.json        paper2_q0113.json            paper2_q0400.json        paper2_q0681.json
 paper1_q0353.json                                        paper1_q0614.json        paper2_q0114.json            paper2_q0401.json        paper2_q0682.json
 paper1_q0354.json                                        paper1_q0615.json        paper2_q0115.json            paper2_q0402.json       'paper2_q0683 (1).json'
'paper1_q0355 (1).json'                                   paper1_q0616.json        paper2_q0116.json            paper2_q0403.json        paper2_q0683.json
 paper1_q0355.json                                        paper1_q0617.json        paper2_q0117.json            paper2_q0404.json        paper2_q0684.json
 paper1_q0356.json                                        paper1_q0618.json        paper2_q0118.json            paper2_q0405.json       'paper2_q0685 (1).json'
 paper1_q0357.json                                        paper1_q0619.json        paper2_q0119.json            paper2_q0406.json        paper2_q0685.json
 paper1_q0358.json                                        paper1_q0620.json        paper2_q0120.json            paper2_q0407.json        prep_syspin.py
 paper1_q0359.json                                        paper1_q0621.json        paper2_q0121.json            paper2_q0408.json        prompts
'paper1_q0360 (1).json'                                   paper1_q0622.json        paper2_q0122.json            paper2_q0409.json        requirements-serve.txt
 paper1_q0360.json                                        paper1_q0623.json        paper2_q0123.json            paper2_q0410.json        requirements-train.txt
'paper1_q0361 (1).json'                                  'paper1_q0624 (1).json'   paper2_q0125.json            paper2_q0411.json        requirements.txt
 paper1_q0361.json                                        paper1_q0624.json        paper2_q0126.json            paper2_q0412.json        rewrite.txt
'paper1_q0362 (1).json'                                   paper1_q0625.json        paper2_q0127.json            paper2_q0413.json        rewrite_raw
 paper1_q0362.json                                       'paper1_q0626 (1).json'   paper2_q0128.json            paper2_q0414.json        rewrite_rejected.jsonl
'paper1_q0363 (1).json'                                   paper1_q0626.json        paper2_q0129.json            paper2_q0415.json        rewrite_surplus.jsonl
 paper1_q0363.json                                        paper1_q0627.json        paper2_q0130.json            paper2_q0416.json        rsetup_candidates.json
 paper1_q0364.json                                        paper1_q0628.json        paper2_q0131.json            paper2_q0417.json        rsetup_filters.cpython-311.pyc
'paper1_q0365 (1).json'                                   paper1_q0629.json        paper2_q0132.json            paper2_q0418.json        rsetup_filters.py
 paper1_q0365.json                                        paper1_q0630.json        paper2_q0133.json            paper2_q0419.json        rsetup_final_pool.json
 paper1_q0366.json                                       'paper1_q0631 (1).json'   paper2_q0134.json            paper2_q0420.json        rsetup_shortlist.json
'paper1_q0367 (1).json'                                   paper1_q0631.json        paper2_q0135.json            paper2_q0421.json        select_rsetup.cpython-311.pyc
 paper1_q0367.json                                        paper1_q0632.json        paper2_q0136.json            paper2_q0422.json        select_rsetup.py
'paper1_q0368 (1).json'                                   paper1_q0633.json        paper2_q0137.json            paper2_q0423.json        setup_instance.sh
 paper1_q0368.json                                        paper1_q0634.json        paper2_q0138.json            paper2_q0424.json        sft_data
 paper1_q0369.json                                        paper1_q0635.json        paper2_q0139.json            paper2_q0425.json        sft_upload
'paper1_q0370 (1).json'                                   paper1_q0636.json        paper2_q0140.json            paper2_q0426.json        stage1_run.log
 paper1_q0370.json                                        paper1_q0637.json        paper2_q0141.json            paper2_q0427.json        stage6_report.txt
'paper1_q0371 (1).json'                                   paper1_q0638.json        paper2_q0142.json            paper2_q0428.json        stage7_gates.txt
 paper1_q0371.json                                       'paper1_q0639 (1).json'   paper2_q0143.json           'paper2_q0429 (1).json'   template_check.txt
'paper1_q0373 (1).json'                                   paper1_q0639.json        paper2_q0144.json            paper2_q0429.json        topup.py
 paper1_q0373.json                                        paper1_q0640.json        paper2_q0145.json           'paper2_q0430 (1).json'   train.jsonl
 paper1_q0374.json                                        paper1_q0641.json        paper2_q0146.json            paper2_q0430.json        train.py
'paper1_q0375 (1).json'                                   paper1_q0642.json        paper2_q0147.json            paper2_q0431.json        tts
 paper1_q0375.json                                        paper1_q0643.json        paper2_q0148.json            paper2_q0432.json        venvs
'paper1_q0376 (1).json'                                   paper1_q0644.json       'paper2_q0149 (1).json'       paper2_q0433.json        verify.py
 paper1_q0376.json                                        paper1_q0645.json        paper2_q0149.json            paper2_q0434.json        verify_concept_facts.py
'paper1_q0377 (1).json'                                   paper1_q0646.json        paper2_q0150.json            paper2_q0435.json
 paper1_q0377.json                                        paper1_q0647.json       'paper2_q0151 (1).json'       paper2_q0436.json

/home/ec2-user/SageMaker/tts:
logs  scripts
```

---

## Paste 02  (transcript user message #123, 2026-10-18T04:55:48.841Z)

```
(base) [ec2-user@ip-REDACTED pocket-tts]$ mkdir -p ~/SageMaker/tts/data/raw && aws s3 cp s3://aarav-10x/raw/syspin/IISc_SYSPINProject_Telugu_Male_Spk001_HC.tar.gz - | head -c 2800000000 | tar -xz -C ~/SageMaker/tts/data/raw

gzip: stdin: unexpected end of file
tar: Unexpected EOF in archive
tar: Unexpected EOF in archive
tar: Error is not recoverable: exiting now
download failed: s3://aarav-10x/raw/syspin/IISc_SYSPINProject_Telugu_Male_Spk001_HC.tar.gz to - [Errno 32] Broken pipe
(base) [ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 03  (transcript user message #129, 2026-10-18T05:26:23.978Z)

```
[ec2-user@ip-REDACTED ~]$ rm -rf ~/SageMaker/tts/data/raw && df -h ~/SageMaker | tail -1
/dev/nvme2n1     40G   21G   17G  57% /home/ec2-user/SageMaker
[ec2-user@ip-REDACTED ~]$ source ~/SageMaker/tts/env.sh && cat ~/SageMaker/tts/data/pilot/stats.json && wc -l ~/SageMaker/tts/data/pilot/*.jsonl && du -sh ~/SageMaker/tts/data/pilot
{
  "clips_in_json": 21463,
  "kept": 2283,
  "train": 2246,
  "valid": 37,
  "hours_kept": 5.026,
  "rejected": 18920,
  "reject_reasons": {
    "missing_wav": 18413,
    "digits": 412,
    "chars": 10,
    "ffmpeg": 85
  },
  "domains_selected": {
    "POLITICS": 206,
    "FINANCE": 206,
    "WEATHER": 83,
    "HEALTH": 85,
    "EDUCATION": 219,
    "RUNNING TEXT FROM BOOK": 363,
    "BOOKS": 1149,
    "OTHERS": 79,
    "GENERAL": 143,
    "AGRICULTURE": 95
  }
}  2246 /home/ec2-user/SageMaker/tts/data/pilot/train.jsonl
    37 /home/ec2-user/SageMaker/tts/data/pilot/valid.jsonl
  2283 total
846M    /home/ec2-user/SageMaker/tts/data/pilot
[ec2-user@ip-REDACTED ~]$ cd ~/SageMaker/tts/pocket-tts && uv run python -c "import torch; print('cuda available:', torch.cuda.is_available(), '|', torch.cuda.get_device_name(0))"
cuda available: True | NVIDIA A10G
[ec2-user@ip-REDACTED pocket-tts]$ cd ~/SageMaker/tts/pocket-tts && uv run hf auth login
User is already logged in. Use `hf auth login --force` to force re-login.
[ec2-user@ip-REDACTED pocket-tts]$ uv run python -m training.scripts.align_data --help
                                                                                                                                                                                       
 Usage: python -m training.scripts.align_data [OPTIONS] {input_jsonl}                                                                                                                  
                                              {output_jsonl}                                                                                                                           
                                                                                                                                                                                       
╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    input_jsonl       <str>  [required]                                                                                                                                            │
│ *    output_jsonl      <str>  [required]                                                                                                                                            │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --model                                <str>  [default: facebook/wav2vec2-base-960h]                                                                                                │
│ --resume                --no-resume           append to output_jsonl, skipping the utterances it already holds -- lets preemptible jobs continue where they were killed             │
│                                               [default: no-resume]                                                                                                                  │
│ --device                               <str>  [default: cuda]                                                                                                                       │
│ --shard                                <int>  shard index, used to place the progress bar                                                                                           │
│ --batch-size                           <int>  [default: 32]                                                                                                                         │
│ --sort-window                          <int>  utterances buffered and length-sorted before batching (less padding); output order is restored per window [default: 256]              │
│ --install-completion                          Install completion for the current shell.                                                                                             │
│ --show-completion                             Show completion for the current shell, to copy it or customize the installation.                                                      │
│ --help                                        Show this message and exit.                                                                                                           │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

[ec2-user@ip-REDACTED pocket-tts]$ source ~/SageMaker/tts/env.sh && cd ~/SageMaker/tts/pocket-tts && uv run python -m training.scripts.align_data ~/SageMaker/tts/data/pilot/train.jsonl ~/SageMaker/tts/data/pilot/train_aligned.jsonl --model anuragshas/wav2vec2-large-xlsr-53-telugu --device cuda 2>&1 | tee -a ~/SageMaker/tts/logs/align.log
Loading weights: 100%|██████████| 424/424 [00:00<00:00, 16248.23it/s]
align:   0%|          | 0.0/4.9h [00:00<?, ?h/s]Unable to load any of {libcudnn_engines_runtime_compiled.so.9.24.0, libcudnn_engines_runtime_compiled.so.9.24, libcudnn_engines_runtime_compiled.so.9, libcudnn_engines_runtime_compiled.so}.
Exception in thread Thread-1 (read_entries):
Traceback (most recent call last):
  File "/home/ec2-user/SageMaker/tts/uv-python/cpython-3.10-linux-x86_64-gnu/lib/python3.10/threading.py", line 1016, in _bootstrap_inner
    self.run()
  File "/home/ec2-user/SageMaker/tts/uv-python/cpython-3.10-linux-x86_64-gnu/lib/python3.10/threading.py", line 953, in run
    self._target(*self._args, **self._kwargs)
  File "/home/ec2-user/SageMaker/tts/pocket-tts/training/scripts/align_data.py", line 253, in read_entries
    for line in fin:
ValueError: I/O operation on closed file.
╭───────────────────────────────────────────────────────────────────────── Traceback (most recent call last) ─────────────────────────────────────────────────────────────────────────╮
│ /home/ec2-user/SageMaker/tts/pocket-tts/training/scripts/align_data.py:331 in main                                                                                                  │
│                                                                                                                                                                                     │
│   328 │   │   │   │   │   x[b, : lens[b]] = torch.from_numpy(u[2])                                                                                                                  │
│   329 │   │   │   │   attn = (torch.arange(max(lens))[None, :] < torch.tensor(lens)[:, None]).long()                                                                                │
│   330 │   │   │   │   with torch.no_grad():                                                                                                                                         │
│ ❱ 331 │   │   │   │   │   logits = ctc_model(                                                                                                                                       │
│   332 │   │   │   │   │   │   x.to(device_t, torch.bfloat16 if use_bf16 else torch.float32),                                                                                        │
│   333 │   │   │   │   │   │   attention_mask=attn.to(device_t),                                                                                                                     │
│   334 │   │   │   │   │   ).logits.float()                                                                                                                                          │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/module.py:1783 in _wrapped_call_impl                                                    │
│                                                                                                                                                                                     │
│   1780 │   │   if self._compiled_call_impl is not None:                                                                                                                             │
│   1781 │   │   │   return self._compiled_call_impl(*args, **kwargs)  # type: ignore[misc]                                                                                           │
│   1782 │   │   else:                                                                                                                                                                │
│ ❱ 1783 │   │   │   return self._call_impl(*args, **kwargs)                                                                                                                          │
│   1784 │                                                                                                                                                                            │
│   1785 │   # torchrec tests the code consistency with the following code                                                                                                            │
│   1786 │   # fmt: off                                                                                                                                                               │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/module.py:1794 in _call_impl                                                            │
│                                                                                                                                                                                     │
│   1791 │   │   if not (self._backward_hooks or self._backward_pre_hooks or self._forward_hooks or self._forward_pre_hooks                                                           │
│   1792 │   │   │   │   or _global_backward_pre_hooks or _global_backward_hooks                                                                                                      │
│   1793 │   │   │   │   or _global_forward_hooks or _global_forward_pre_hooks):                                                                                                      │
│ ❱ 1794 │   │   │   return forward_call(*args, **kwargs)                                                                                                                             │
│   1795 │   │                                                                                                                                                                        │
│   1796 │   │   result = None                                                                                                                                                        │
│   1797 │   │   called_always_called_hooks = set()                                                                                                                                   │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/transformers/utils/generic.py:939 in wrapper                                                             │
│                                                                                                                                                                                     │
│    936 │   │   return_dict_passed = kwargs.pop("return_dict", return_dict)                                                                                                          │
│    937 │   │   if return_dict_passed is not None:                                                                                                                                   │
│    938 │   │   │   return_dict = return_dict_passed                                                                                                                                 │
│ ❱  939 │   │   output = func(self, *args, **kwargs)                                                                                                                                 │
│    940 │   │   if not return_dict and not isinstance(output, tuple):                                                                                                                │
│    941 │   │   │   output = output.to_tuple()                                                                                                                                       │
│    942 │   │   return output                                                                                                                                                        │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/transformers/models/wav2vec2/modeling_wav2vec2.py:1606 in forward                                        │
│                                                                                                                                                                                     │
│   1603 │   │   if labels is not None and labels.max() >= self.config.vocab_size:                                                                                                    │
│   1604 │   │   │   raise ValueError(f"Label values must be <= vocab_size: {self.config.vocab_size}")                                                                                │
│   1605 │   │                                                                                                                                                                        │
│ ❱ 1606 │   │   outputs = self.wav2vec2(                                                                                                                                             │
│   1607 │   │   │   input_values,                                                                                                                                                    │
│   1608 │   │   │   attention_mask=attention_mask,                                                                                                                                   │
│   1609 │   │   │   **kwargs,                                                                                                                                                        │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/module.py:1783 in _wrapped_call_impl                                                    │
│                                                                                                                                                                                     │
│   1780 │   │   if self._compiled_call_impl is not None:                                                                                                                             │
│   1781 │   │   │   return self._compiled_call_impl(*args, **kwargs)  # type: ignore[misc]                                                                                           │
│   1782 │   │   else:                                                                                                                                                                │
│ ❱ 1783 │   │   │   return self._call_impl(*args, **kwargs)                                                                                                                          │
│   1784 │                                                                                                                                                                            │
│   1785 │   # torchrec tests the code consistency with the following code                                                                                                            │
│   1786 │   # fmt: off                                                                                                                                                               │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/module.py:1794 in _call_impl                                                            │
│                                                                                                                                                                                     │
│   1791 │   │   if not (self._backward_hooks or self._backward_pre_hooks or self._forward_hooks or self._forward_pre_hooks                                                           │
│   1792 │   │   │   │   or _global_backward_pre_hooks or _global_backward_hooks                                                                                                      │
│   1793 │   │   │   │   or _global_forward_hooks or _global_forward_pre_hooks):                                                                                                      │
│ ❱ 1794 │   │   │   return forward_call(*args, **kwargs)                                                                                                                             │
│   1795 │   │                                                                                                                                                                        │
│   1796 │   │   result = None                                                                                                                                                        │
│   1797 │   │   called_always_called_hooks = set()                                                                                                                                   │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/transformers/utils/generic.py:1068 in wrapper                                                            │
│                                                                                                                                                                                     │
│   1065 │   │   │   │   ):                                                                                                                                                           │
│   1066 │   │   │   │   │   output = func(self, *args, **kwargs)                                                                                                                     │
│   1067 │   │   │   else:                                                                                                                                                            │
│ ❱ 1068 │   │   │   │   output = func(self, *args, **kwargs)                                                                                                                         │
│   1069 │   │   # Restore original config value                                                                                                                                      │
│   1070 │   │   finally:                                                                                                                                                             │
│   1071 │   │   │   if is_causal is not None:                                                                                                                                        │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/transformers/utils/output_capturing.py:286 in wrapper                                                    │
│                                                                                                                                                                                     │
│   283 │   │   │                                                                                                                                                                     │
│   284 │   │   │   # Run the forward                                                                                                                                                 │
│   285 │   │   │   try:                                                                                                                                                              │
│ ❱ 286 │   │   │   │   outputs = func(self, *args, **kwargs)                                                                                                                         │
│   287 │   │   │   # Reset the states                                                                                                                                                │
│   288 │   │   │   finally:                                                                                                                                                          │
│   289 │   │   │   │   _active_collector.reset(output_token)                                                                                                                         │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/transformers/models/wav2vec2/modeling_wav2vec2.py:1279 in forward                                        │
│                                                                                                                                                                                     │
│   1276 │   │   │   Indices to mask extracted features for contrastive loss. When in training mode, model learns to predict                                                          │
│   1277 │   │   │   masked extracted features in *config.proj_codevector_dim* space.                                                                                                 │
│   1278 │   │   """                                                                                                                                                                  │
│ ❱ 1279 │   │   extract_features = self.feature_extractor(input_values)                                                                                                              │
│   1280 │   │   extract_features = extract_features.transpose(1, 2)                                                                                                                  │
│   1281 │   │                                                                                                                                                                        │
│   1282 │   │   if attention_mask is not None:                                                                                                                                       │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/module.py:1783 in _wrapped_call_impl                                                    │
│                                                                                                                                                                                     │
│   1780 │   │   if self._compiled_call_impl is not None:                                                                                                                             │
│   1781 │   │   │   return self._compiled_call_impl(*args, **kwargs)  # type: ignore[misc]                                                                                           │
│   1782 │   │   else:                                                                                                                                                                │
│ ❱ 1783 │   │   │   return self._call_impl(*args, **kwargs)                                                                                                                          │
│   1784 │                                                                                                                                                                            │
│   1785 │   # torchrec tests the code consistency with the following code                                                                                                            │
│   1786 │   # fmt: off                                                                                                                                                               │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/module.py:1794 in _call_impl                                                            │
│                                                                                                                                                                                     │
│   1791 │   │   if not (self._backward_hooks or self._backward_pre_hooks or self._forward_hooks or self._forward_pre_hooks                                                           │
│   1792 │   │   │   │   or _global_backward_pre_hooks or _global_backward_hooks                                                                                                      │
│   1793 │   │   │   │   or _global_forward_hooks or _global_forward_pre_hooks):                                                                                                      │
│ ❱ 1794 │   │   │   return forward_call(*args, **kwargs)                                                                                                                             │
│   1795 │   │                                                                                                                                                                        │
│   1796 │   │   result = None                                                                                                                                                        │
│   1797 │   │   called_always_called_hooks = set()                                                                                                                                   │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/transformers/models/wav2vec2/modeling_wav2vec2.py:420 in forward                                         │
│                                                                                                                                                                                     │
│    417 │   │   │   hidden_states.requires_grad = True                                                                                                                               │
│    418 │   │                                                                                                                                                                        │
│    419 │   │   for conv_layer in self.conv_layers:                                                                                                                                  │
│ ❱  420 │   │   │   hidden_states = conv_layer(hidden_states)                                                                                                                        │
│    421 │   │                                                                                                                                                                        │
│    422 │   │   return hidden_states                                                                                                                                                 │
│    423                                                                                                                                                                              │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/transformers/modeling_layers.py:109 in __call__                                                          │
│                                                                                                                                                                                     │
│   106 │   │   │   │   logger.warning_once(message)                                                                                                                                  │
│   107 │   │   │                                                                                                                                                                     │
│   108 │   │   │   return self._gradient_checkpointing_func(partial(super().__call__, **kwargs), *args)                                                                              │
│ ❱ 109 │   │   return super().__call__(*args, **kwargs)                                                                                                                              │
│   110                                                                                                                                                                               │
│   111                                                                                                                                                                               │
│   112 @auto_docstring                                                                                                                                                               │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/module.py:1783 in _wrapped_call_impl                                                    │
│                                                                                                                                                                                     │
│   1780 │   │   if self._compiled_call_impl is not None:                                                                                                                             │
│   1781 │   │   │   return self._compiled_call_impl(*args, **kwargs)  # type: ignore[misc]                                                                                           │
│   1782 │   │   else:                                                                                                                                                                │
│ ❱ 1783 │   │   │   return self._call_impl(*args, **kwargs)                                                                                                                          │
│   1784 │                                                                                                                                                                            │
│   1785 │   # torchrec tests the code consistency with the following code                                                                                                            │
│   1786 │   # fmt: off                                                                                                                                                               │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/module.py:1794 in _call_impl                                                            │
│                                                                                                                                                                                     │
│   1791 │   │   if not (self._backward_hooks or self._backward_pre_hooks or self._forward_hooks or self._forward_pre_hooks                                                           │
│   1792 │   │   │   │   or _global_backward_pre_hooks or _global_backward_hooks                                                                                                      │
│   1793 │   │   │   │   or _global_forward_hooks or _global_forward_pre_hooks):                                                                                                      │
│ ❱ 1794 │   │   │   return forward_call(*args, **kwargs)                                                                                                                             │
│   1795 │   │                                                                                                                                                                        │
│   1796 │   │   result = None                                                                                                                                                        │
│   1797 │   │   called_always_called_hooks = set()                                                                                                                                   │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/transformers/models/wav2vec2/modeling_wav2vec2.py:295 in forward                                         │
│                                                                                                                                                                                     │
│    292 │   │   self.activation = ACT2FN[config.feat_extract_activation]                                                                                                             │
│    293 │                                                                                                                                                                            │
│    294 │   def forward(self, hidden_states):                                                                                                                                        │
│ ❱  295 │   │   hidden_states = self.conv(hidden_states)                                                                                                                             │
│    296 │   │                                                                                                                                                                        │
│    297 │   │   hidden_states = hidden_states.transpose(-2, -1)                                                                                                                      │
│    298 │   │   hidden_states = self.layer_norm(hidden_states)                                                                                                                       │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/module.py:1783 in _wrapped_call_impl                                                    │
│                                                                                                                                                                                     │
│   1780 │   │   if self._compiled_call_impl is not None:                                                                                                                             │
│   1781 │   │   │   return self._compiled_call_impl(*args, **kwargs)  # type: ignore[misc]                                                                                           │
│   1782 │   │   else:                                                                                                                                                                │
│ ❱ 1783 │   │   │   return self._call_impl(*args, **kwargs)                                                                                                                          │
│   1784 │                                                                                                                                                                            │
│   1785 │   # torchrec tests the code consistency with the following code                                                                                                            │
│   1786 │   # fmt: off                                                                                                                                                               │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/module.py:1794 in _call_impl                                                            │
│                                                                                                                                                                                     │
│   1791 │   │   if not (self._backward_hooks or self._backward_pre_hooks or self._forward_hooks or self._forward_pre_hooks                                                           │
│   1792 │   │   │   │   or _global_backward_pre_hooks or _global_backward_hooks                                                                                                      │
│   1793 │   │   │   │   or _global_forward_hooks or _global_forward_pre_hooks):                                                                                                      │
│ ❱ 1794 │   │   │   return forward_call(*args, **kwargs)                                                                                                                             │
│   1795 │   │                                                                                                                                                                        │
│   1796 │   │   result = None                                                                                                                                                        │
│   1797 │   │   called_always_called_hooks = set()                                                                                                                                   │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/conv.py:385 in forward                                                                  │
│                                                                                                                                                                                     │
│    382 │   │   )                                                                                                                                                                    │
│    383 │                                                                                                                                                                            │
│    384 │   def forward(self, input: Tensor) -> Tensor:                                                                                                                              │
│ ❱  385 │   │   return self._conv_forward(input, self.weight, self.bias)                                                                                                             │
│    386                                                                                                                                                                              │
│    387                                                                                                                                                                              │
│    388 class Conv2d(_ConvNd):                                                                                                                                                       │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/conv.py:380 in _conv_forward                                                            │
│                                                                                                                                                                                     │
│    377 │   │   │   │   self.groups,                                                                                                                                                 │
│    378 │   │   │   )                                                                                                                                                                │
│    379 │   │                                                                                                                                                                        │
│ ❱  380 │   │   return F.conv1d(                                                                                                                                                     │
│    381 │   │   │   input, weight, bias, self.stride, self.padding, self.dilation, self.groups                                                                                       │
│    382 │   │   )                                                                                                                                                                    │
│    383                                                                                                                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
RuntimeError: CUDNN_BACKEND_TENSOR_DESCRIPTOR cudnnFinalize failedptrDesc->finalize() cudnn_status: CUDNN_STATUS_SUBLIBRARY_LOADING_FAILED
align:   0%|          | 0.0/4.9h [00:09<?, ?h/s]
[ec2-user@ip-REDACTED pocket-tts]$ uv run python -m training.scripts.align_data ~/SageMaker/tts/data/pilot/valid.jsonl ~/SageMaker/tts/data/pilot/valid_aligned.jsonl --model anuragshas/wav2vec2-large-xlsr-53-telugu --device cuda 2>&1 | tee -a ~/SageMaker/tts/logs/align.log
Loading weights: 100%|██████████| 424/424 [00:00<00:00, 14483.38it/s]
align:   0%|          | 0.0/0.1h [00:00<?, ?h/s]Unable to load any of {libcudnn_engines_runtime_compiled.so.9.24.0, libcudnn_engines_runtime_compiled.so.9.24, libcudnn_engines_runtime_compiled.so.9, libcudnn_engines_runtime_compiled.so}.
╭───────────────────────────────────────────────────────────────────────── Traceback (most recent call last) ─────────────────────────────────────────────────────────────────────────╮
│ /home/ec2-user/SageMaker/tts/pocket-tts/training/scripts/align_data.py:331 in main                                                                                                  │
│                                                                                                                                                                                     │
│   328 │   │   │   │   │   x[b, : lens[b]] = torch.from_numpy(u[2])                                                                                                                  │
│   329 │   │   │   │   attn = (torch.arange(max(lens))[None, :] < torch.tensor(lens)[:, None]).long()                                                                                │
│   330 │   │   │   │   with torch.no_grad():                                                                                                                                         │
│ ❱ 331 │   │   │   │   │   logits = ctc_model(                                                                                                                                       │
│   332 │   │   │   │   │   │   x.to(device_t, torch.bfloat16 if use_bf16 else torch.float32),                                                                                        │
│   333 │   │   │   │   │   │   attention_mask=attn.to(device_t),                                                                                                                     │
│   334 │   │   │   │   │   ).logits.float()                                                                                                                                          │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/module.py:1783 in _wrapped_call_impl                                                    │
│                                                                                                                                                                                     │
│   1780 │   │   if self._compiled_call_impl is not None:                                                                                                                             │
│   1781 │   │   │   return self._compiled_call_impl(*args, **kwargs)  # type: ignore[misc]                                                                                           │
│   1782 │   │   else:                                                                                                                                                                │
│ ❱ 1783 │   │   │   return self._call_impl(*args, **kwargs)                                                                                                                          │
│   1784 │                                                                                                                                                                            │
│   1785 │   # torchrec tests the code consistency with the following code                                                                                                            │
│   1786 │   # fmt: off                                                                                                                                                               │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/module.py:1794 in _call_impl                                                            │
│                                                                                                                                                                                     │
│   1791 │   │   if not (self._backward_hooks or self._backward_pre_hooks or self._forward_hooks or self._forward_pre_hooks                                                           │
│   1792 │   │   │   │   or _global_backward_pre_hooks or _global_backward_hooks                                                                                                      │
│   1793 │   │   │   │   or _global_forward_hooks or _global_forward_pre_hooks):                                                                                                      │
│ ❱ 1794 │   │   │   return forward_call(*args, **kwargs)                                                                                                                             │
│   1795 │   │                                                                                                                                                                        │
│   1796 │   │   result = None                                                                                                                                                        │
│   1797 │   │   called_always_called_hooks = set()                                                                                                                                   │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/transformers/utils/generic.py:939 in wrapper                                                             │
│                                                                                                                                                                                     │
│    936 │   │   return_dict_passed = kwargs.pop("return_dict", return_dict)                                                                                                          │
│    937 │   │   if return_dict_passed is not None:                                                                                                                                   │
│    938 │   │   │   return_dict = return_dict_passed                                                                                                                                 │
│ ❱  939 │   │   output = func(self, *args, **kwargs)                                                                                                                                 │
│    940 │   │   if not return_dict and not isinstance(output, tuple):                                                                                                                │
│    941 │   │   │   output = output.to_tuple()                                                                                                                                       │
│    942 │   │   return output                                                                                                                                                        │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/transformers/models/wav2vec2/modeling_wav2vec2.py:1606 in forward                                        │
│                                                                                                                                                                                     │
│   1603 │   │   if labels is not None and labels.max() >= self.config.vocab_size:                                                                                                    │
│   1604 │   │   │   raise ValueError(f"Label values must be <= vocab_size: {self.config.vocab_size}")                                                                                │
│   1605 │   │                                                                                                                                                                        │
│ ❱ 1606 │   │   outputs = self.wav2vec2(                                                                                                                                             │
│   1607 │   │   │   input_values,                                                                                                                                                    │
│   1608 │   │   │   attention_mask=attention_mask,                                                                                                                                   │
│   1609 │   │   │   **kwargs,                                                                                                                                                        │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/module.py:1783 in _wrapped_call_impl                                                    │
│                                                                                                                                                                                     │
│   1780 │   │   if self._compiled_call_impl is not None:                                                                                                                             │
│   1781 │   │   │   return self._compiled_call_impl(*args, **kwargs)  # type: ignore[misc]                                                                                           │
│   1782 │   │   else:                                                                                                                                                                │
│ ❱ 1783 │   │   │   return self._call_impl(*args, **kwargs)                                                                                                                          │
│   1784 │                                                                                                                                                                            │
│   1785 │   # torchrec tests the code consistency with the following code                                                                                                            │
│   1786 │   # fmt: off                                                                                                                                                               │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/module.py:1794 in _call_impl                                                            │
│                                                                                                                                                                                     │
│   1791 │   │   if not (self._backward_hooks or self._backward_pre_hooks or self._forward_hooks or self._forward_pre_hooks                                                           │
│   1792 │   │   │   │   or _global_backward_pre_hooks or _global_backward_hooks                                                                                                      │
│   1793 │   │   │   │   or _global_forward_hooks or _global_forward_pre_hooks):                                                                                                      │
│ ❱ 1794 │   │   │   return forward_call(*args, **kwargs)                                                                                                                             │
│   1795 │   │                                                                                                                                                                        │
│   1796 │   │   result = None                                                                                                                                                        │
│   1797 │   │   called_always_called_hooks = set()                                                                                                                                   │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/transformers/utils/generic.py:1068 in wrapper                                                            │
│                                                                                                                                                                                     │
│   1065 │   │   │   │   ):                                                                                                                                                           │
│   1066 │   │   │   │   │   output = func(self, *args, **kwargs)                                                                                                                     │
│   1067 │   │   │   else:                                                                                                                                                            │
│ ❱ 1068 │   │   │   │   output = func(self, *args, **kwargs)                                                                                                                         │
│   1069 │   │   # Restore original config value                                                                                                                                      │
│   1070 │   │   finally:                                                                                                                                                             │
│   1071 │   │   │   if is_causal is not None:                                                                                                                                        │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/transformers/utils/output_capturing.py:286 in wrapper                                                    │
│                                                                                                                                                                                     │
│   283 │   │   │                                                                                                                                                                     │
│   284 │   │   │   # Run the forward                                                                                                                                                 │
│   285 │   │   │   try:                                                                                                                                                              │
│ ❱ 286 │   │   │   │   outputs = func(self, *args, **kwargs)                                                                                                                         │
│   287 │   │   │   # Reset the states                                                                                                                                                │
│   288 │   │   │   finally:                                                                                                                                                          │
│   289 │   │   │   │   _active_collector.reset(output_token)                                                                                                                         │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/transformers/models/wav2vec2/modeling_wav2vec2.py:1279 in forward                                        │
│                                                                                                                                                                                     │
│   1276 │   │   │   Indices to mask extracted features for contrastive loss. When in training mode, model learns to predict                                                          │
│   1277 │   │   │   masked extracted features in *config.proj_codevector_dim* space.                                                                                                 │
│   1278 │   │   """                                                                                                                                                                  │
│ ❱ 1279 │   │   extract_features = self.feature_extractor(input_values)                                                                                                              │
│   1280 │   │   extract_features = extract_features.transpose(1, 2)                                                                                                                  │
│   1281 │   │                                                                                                                                                                        │
│   1282 │   │   if attention_mask is not None:                                                                                                                                       │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/module.py:1783 in _wrapped_call_impl                                                    │
│                                                                                                                                                                                     │
│   1780 │   │   if self._compiled_call_impl is not None:                                                                                                                             │
│   1781 │   │   │   return self._compiled_call_impl(*args, **kwargs)  # type: ignore[misc]                                                                                           │
│   1782 │   │   else:                                                                                                                                                                │
│ ❱ 1783 │   │   │   return self._call_impl(*args, **kwargs)                                                                                                                          │
│   1784 │                                                                                                                                                                            │
│   1785 │   # torchrec tests the code consistency with the following code                                                                                                            │
│   1786 │   # fmt: off                                                                                                                                                               │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/module.py:1794 in _call_impl                                                            │
│                                                                                                                                                                                     │
│   1791 │   │   if not (self._backward_hooks or self._backward_pre_hooks or self._forward_hooks or self._forward_pre_hooks                                                           │
│   1792 │   │   │   │   or _global_backward_pre_hooks or _global_backward_hooks                                                                                                      │
│   1793 │   │   │   │   or _global_forward_hooks or _global_forward_pre_hooks):                                                                                                      │
│ ❱ 1794 │   │   │   return forward_call(*args, **kwargs)                                                                                                                             │
│   1795 │   │                                                                                                                                                                        │
│   1796 │   │   result = None                                                                                                                                                        │
│   1797 │   │   called_always_called_hooks = set()                                                                                                                                   │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/transformers/models/wav2vec2/modeling_wav2vec2.py:420 in forward                                         │
│                                                                                                                                                                                     │
│    417 │   │   │   hidden_states.requires_grad = True                                                                                                                               │
│    418 │   │                                                                                                                                                                        │
│    419 │   │   for conv_layer in self.conv_layers:                                                                                                                                  │
│ ❱  420 │   │   │   hidden_states = conv_layer(hidden_states)                                                                                                                        │
│    421 │   │                                                                                                                                                                        │
│    422 │   │   return hidden_states                                                                                                                                                 │
│    423                                                                                                                                                                              │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/transformers/modeling_layers.py:109 in __call__                                                          │
│                                                                                                                                                                                     │
│   106 │   │   │   │   logger.warning_once(message)                                                                                                                                  │
│   107 │   │   │                                                                                                                                                                     │
│   108 │   │   │   return self._gradient_checkpointing_func(partial(super().__call__, **kwargs), *args)                                                                              │
│ ❱ 109 │   │   return super().__call__(*args, **kwargs)                                                                                                                              │
│   110                                                                                                                                                                               │
│   111                                                                                                                                                                               │
│   112 @auto_docstring                                                                                                                                                               │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/module.py:1783 in _wrapped_call_impl                                                    │
│                                                                                                                                                                                     │
│   1780 │   │   if self._compiled_call_impl is not None:                                                                                                                             │
│   1781 │   │   │   return self._compiled_call_impl(*args, **kwargs)  # type: ignore[misc]                                                                                           │
│   1782 │   │   else:                                                                                                                                                                │
│ ❱ 1783 │   │   │   return self._call_impl(*args, **kwargs)                                                                                                                          │
│   1784 │                                                                                                                                                                            │
│   1785 │   # torchrec tests the code consistency with the following code                                                                                                            │
│   1786 │   # fmt: off                                                                                                                                                               │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/module.py:1794 in _call_impl                                                            │
│                                                                                                                                                                                     │
│   1791 │   │   if not (self._backward_hooks or self._backward_pre_hooks or self._forward_hooks or self._forward_pre_hooks                                                           │
│   1792 │   │   │   │   or _global_backward_pre_hooks or _global_backward_hooks                                                                                                      │
│   1793 │   │   │   │   or _global_forward_hooks or _global_forward_pre_hooks):                                                                                                      │
│ ❱ 1794 │   │   │   return forward_call(*args, **kwargs)                                                                                                                             │
│   1795 │   │                                                                                                                                                                        │
│   1796 │   │   result = None                                                                                                                                                        │
│   1797 │   │   called_always_called_hooks = set()                                                                                                                                   │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/transformers/models/wav2vec2/modeling_wav2vec2.py:295 in forward                                         │
│                                                                                                                                                                                     │
│    292 │   │   self.activation = ACT2FN[config.feat_extract_activation]                                                                                                             │
│    293 │                                                                                                                                                                            │
│    294 │   def forward(self, hidden_states):                                                                                                                                        │
│ ❱  295 │   │   hidden_states = self.conv(hidden_states)                                                                                                                             │
│    296 │   │                                                                                                                                                                        │
│    297 │   │   hidden_states = hidden_states.transpose(-2, -1)                                                                                                                      │
│    298 │   │   hidden_states = self.layer_norm(hidden_states)                                                                                                                       │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/module.py:1783 in _wrapped_call_impl                                                    │
│                                                                                                                                                                                     │
│   1780 │   │   if self._compiled_call_impl is not None:                                                                                                                             │
│   1781 │   │   │   return self._compiled_call_impl(*args, **kwargs)  # type: ignore[misc]                                                                                           │
│   1782 │   │   else:                                                                                                                                                                │
│ ❱ 1783 │   │   │   return self._call_impl(*args, **kwargs)                                                                                                                          │
│   1784 │                                                                                                                                                                            │
│   1785 │   # torchrec tests the code consistency with the following code                                                                                                            │
│   1786 │   # fmt: off                                                                                                                                                               │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/module.py:1794 in _call_impl                                                            │
│                                                                                                                                                                                     │
│   1791 │   │   if not (self._backward_hooks or self._backward_pre_hooks or self._forward_hooks or self._forward_pre_hooks                                                           │
│   1792 │   │   │   │   or _global_backward_pre_hooks or _global_backward_hooks                                                                                                      │
│   1793 │   │   │   │   or _global_forward_hooks or _global_forward_pre_hooks):                                                                                                      │
│ ❱ 1794 │   │   │   return forward_call(*args, **kwargs)                                                                                                                             │
│   1795 │   │                                                                                                                                                                        │
│   1796 │   │   result = None                                                                                                                                                        │
│   1797 │   │   called_always_called_hooks = set()                                                                                                                                   │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/conv.py:385 in forward                                                                  │
│                                                                                                                                                                                     │
│    382 │   │   )                                                                                                                                                                    │
│    383 │                                                                                                                                                                            │
│    384 │   def forward(self, input: Tensor) -> Tensor:                                                                                                                              │
│ ❱  385 │   │   return self._conv_forward(input, self.weight, self.bias)                                                                                                             │
│    386                                                                                                                                                                              │
│    387                                                                                                                                                                              │
│    388 class Conv2d(_ConvNd):                                                                                                                                                       │
│                                                                                                                                                                                     │
│ /home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/modules/conv.py:380 in _conv_forward                                                            │
│                                                                                                                                                                                     │
│    377 │   │   │   │   self.groups,                                                                                                                                                 │
│    378 │   │   │   )                                                                                                                                                                │
│    379 │   │                                                                                                                                                                        │
│ ❱  380 │   │   return F.conv1d(                                                                                                                                                     │
│    381 │   │   │   input, weight, bias, self.stride, self.padding, self.dilation, self.groups                                                                                       │
│    382 │   │   )                                                                                                                                                                    │
│    383                                                                                                                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
RuntimeError: CUDNN_BACKEND_TENSOR_DESCRIPTOR cudnnFinalize failedptrDesc->finalize() cudnn_status: CUDNN_STATUS_SUBLIBRARY_LOADING_FAILED
align:   0%|          | 0.0/0.1h [00:01<?, ?h/s]
```

---

## Paste 04  (transcript user message #131, 2026-10-18T05:36:50.138Z)

```
ec2-user@ip-REDACTED pocket-tts]$ echo "LD_LIBRARY_PATH=$LD_LIBRARY_PATH"
LD_LIBRARY_PATH=/usr/local/cuda-13.2/lib:/usr/local/cuda-13.2/lib64:/usr/local/cuda-13.2:/usr/local/cuda-13.2/targets/x86_64-linux/lib/:/usr/local/cuda-13.2/extras/CUPTI/lib64:/opt/amazon/openmpi/lib64:/opt/amazon/efa/lib64:/opt/amazon/ofi-nccl/lib64:/usr/local/lib:/usr/lib:/lib:/usr/local/cuda-13.2/lib:/usr/local/cuda-13.2/lib64:/usr/local/cuda-13.2:/usr/local/cuda-13.2/targets/x86_64-linux/lib/:/usr/local/cuda-13.2/extras/CUPTI/lib64:/opt/amazon/openmpi/lib64:/opt/amazon/efa/lib64:/opt/amazon/ofi-nccl/lib64:/usr/local/lib:/usr/lib:/lib
[ec2-user@ip-REDACTED pocket-tts]$ cd ~/SageMaker/tts/pocket-tts && env -u LD_LIBRARY_PATH uv run python -c "import torch; x=torch.randn(1,1,16000,device='cuda'); w=torch.randn(4,1,10,device='cuda'); print('conv ok', torch.nn.functional.conv1d(x,w).shape)"
conv ok torch.Size([1, 4, 15991])
[ec2-user@ip-REDACTED pocket-tts]$ cd ~/SageMaker/tts/pocket-tts && env -u LD_LIBRARY_PATH uv run python -m training.scripts.align_data ~/SageMaker/tts/data/pilot/valid.jsonl ~/SageMaker/tts/data/pilot/valid_aligned.jsonl --model anuragshas/wav2vec2-large-xlsr-53-telugu --device cuda 2>&1 | tee -a ~/SageMaker/tts/logs/align.log
Loading weights: 100%|██████████| 424/424 [00:00<00:00, 14103.53it/s]
align:   0%|          | 0.0/0.1h [00:00<?, ?h/s]/home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/tqdm/std.py:636: TqdmWarning: clamping frac to range [0, 1]
  full_bar = Bar(frac,
align: 100%|██████████| 0.1/0.1h [00:01<-00:00, 20.72s/h, ok=37, skipped=0]
[18-10 05:28:55 INFO align] done: 37 aligned, 0 skipped
[ec2-user@ip-REDACTED pocket-tts]$ env -u LD_LIBRARY_PATH uv run python -m training.scripts.align_data ~/SageMaker/tts/data/pilot/train.jsonl ~/SageMaker/tts/data/pilot/train_aligned.jsonl --model anuragshas/wav2vec2-large-xlsr-53-telugu --device cuda 2>&1 | tee -a ~/SageMaker/tts/logs/align.log
Loading weights: 100%|██████████| 424/424 [00:00<00:00, 19191.55it/s]
align:  12%|█▏        | 0.6/4.9h [00:08<01:01, 14.06s/h, ok=256, skipped=0][W1018 05:29:17.081086094 CUDACachingAllocator.cpp:3934] memory allocation failed with OOM on device 0 while trying to allocate 2801795072 bytes (free: 1224146944, total: 23686938624).
align:  23%|██▎       | 1.1/4.9h [00:14<00:47, 12.36s/h, ok=512, skipped=0][18-10 05:29:19 WARNING align] skipping (1 so far): /home/ec2-user/SageMaker/tts/data/pilot/wavs/IISc_SYSPINProject_te_m_FINA_01526.wav: alignment failed
align:  91%|█████████ | 4.5/4.9h [00:50<00:04, 10.85s/h, ok=2047, skipped=1]/home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/tqdm/std.py:636: TqdmWarning: clamping frac to range [0, 1]
  full_bar = Bar(frac,
align: 100%|██████████| 4.9/4.9h [00:55<-00:00, 11.22s/h, ok=2245, skipped=1]
[18-10 05:29:59 INFO align] done: 2245 aligned, 1 skipped
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 05  (transcript user message #133, 2026-10-18T05:42:12.701Z)

```
/home/ec2-user/SageMaker/tts/data/pilot/tokenizer.model
set: ['batch_size', 'ckpt_freq', 'grad_accum_steps', 'max_steps', 'num_ckpt_keep', 'run_dir', 'train_jsonl', 'valid_freq', 'valid_jsonl', 'warmup_steps']
NOT FOUND: ['tokenizer_path']
[18-10 05:41:58 INFO train] logging to /home/ec2-user/SageMaker/tts/runs/telugu_pilot/logs/train_20261018-054157.log
[18-10 05:41:58 INFO train] torch 2.14.0+cu130 | cuda (NVIDIA A10G) | world size 1
[18-10 05:41:58 INFO train] resolved config from training/configs/telugu_pilot.yaml:
data:
  train_jsonl: /home/ec2-user/SageMaker/tts/data/pilot/train_aligned.jsonl
  valid_jsonl: /home/ec2-user/SageMaker/tts/data/pilot/valid_aligned.jsonl
  max_duration_sec: 30.0
  max_voice_prompt_sec: 5.0
  prompt_trim_max_sec: 0.5
  final_punct_dropout: 0.3
  shuffle: true
  loader_procs: 3
  num_bucket_batches: 5
  precompute: true
flow:
  type: lsd
  kwargs: {}
optim:
  lr: 0.0002
  weight_decay: 0.1
  betas:
  - 0.9
  - 0.95
  eps: 1.0e-08
  max_norm: 1.0
  warmup_steps: 50
  schedule: constant
  lr_min_ratio: 0.0
  type: adamw
  muon_lr: 0.005
  muon_momentum: 0.95
  muon_head: false
  muon_rms_match: false
  muon_polar_steps: 6
model_config: pocket_tts/config/english_2026-04_24l.yaml
model_overrides:
  flow_lm.lookup_table.tokenizer_path: data/tokenizer.model
start_from_pretrained: true
freeze_head: false
reset_text_embedding: true
run_dir: /home/ec2-user/SageMaker/tts/runs/telugu_pilot
batch_size: 16
grad_accum_steps: 4
max_steps: 200
seed: 42
flow_batch_multiplier: 4
eos_loss_weight: 0.1
text_dropout: 0.2
voice_dropout: 0.2
stats_ema_steps: 1000
stats_ema_decay: 0.999
log_freq: 50
valid_freq: 100
compile: true
num_valid_batches: 50
sample_sentences:
- The quick brown fox jumps over the lazy dog.
- Training is still running; this voice is a work in progress.
- How much wood would a woodchuck chuck if a woodchuck could chuck wood?
sample_freq: 10000
sample_temp: 0.3
sample_cfg_coef: 2.0
ckpt_freq: 200
num_ckpt_keep: 1
ema_decay: 0.999
distill_cfg_coef: 0.0
distill_teacher_config: ''
distill_teacher_overrides: {}
distill_teacher_weights: ''
distill_teacher_use_ema: true
student_init_from: ''
[18-10 05:41:58 INFO training.dataloader.manifest] indexed 2245 lines of train_aligned.jsonl
[18-10 05:41:58 INFO training.dataloader.manifest] indexed 37 lines of valid_aligned.jsonl
[18-10 05:41:58 INFO pocket_tts.modules.text_conditioner] Loading tokenizers json from data/tokenizer.model
Traceback (most recent call last):
  File "/home/ec2-user/SageMaker/tts/pocket-tts/training/train.py", line 380, in <module>
    main(sys.argv[1])
  File "/home/ec2-user/SageMaker/tts/pocket-tts/training/train.py", line 167, in main
    run = setup(config_path)
  File "/home/ec2-user/SageMaker/tts/pocket-tts/training/train.py", line 117, in setup
    model, mimi, _config = build_models(args)
  File "/home/ec2-user/SageMaker/tts/pocket-tts/training/modules/builders.py", line 151, in build_models
    tts_model = TTSModel._from_pydantic_config(
  File "/home/ec2-user/SageMaker/tts/pocket-tts/pocket_tts/models/tts_model.py", line 143, in _from_pydantic_config
    flow_lm = FlowLMModel.from_pydantic_config(
  File "/home/ec2-user/SageMaker/tts/pocket-tts/pocket_tts/models/flow_lm.py", line 241, in from_pydantic_config
    conditioner = LUTConditioner(
  File "/home/ec2-user/SageMaker/tts/pocket-tts/pocket_tts/modules/text_conditioner.py", line 136, in __init__
    self.tokenizer = build_tokenizer(n_bins, tokenizer_path, tokenizer)
  File "/home/ec2-user/SageMaker/tts/pocket-tts/pocket_tts/modules/text_conditioner.py", line 95, in build_tokenizer
    return JsonTokenizer(nbins, tokenizer_path)
  File "/home/ec2-user/SageMaker/tts/pocket-tts/pocket_tts/modules/text_conditioner.py", line 60, in __init__
    self.tokenizer = tokenizers.Tokenizer.from_file(str(local_path))
Exception: No such file or directory (os error 2)
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 06  (transcript user message #140, 2026-10-18T05:51:24.301Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ source ~/SageMaker/tts/env.sh && cd ~/SageMaker/tts/pocket-tts && env -u LD_LIBRARY_PATH uv run python -m training.scripts.convert_tokenizer ~/SageMaker/tts/data/pilot/tokenizer.model --texts ~/SageMaker/tts/data/pilot/valid_aligned.jsonl 2>&1 | tail -8 \
&& ls -la ~/SageMaker/tts/data/pilot/tokenizer.json \
&& env -u LD_LIBRARY_PATH uv run python -c "
import os, yaml
p='training/configs/telugu_pilot.yaml'
c=yaml.safe_load(open(p))
c['model_overrides']['flow_lm.lookup_table.tokenizer_path']=os.path.expanduser('~/SageMaker/tts/data/pilot/tokenizer.json')
yaml.safe_dump(c,open(p,'w'),sort_keys=False)
print('tokenizer path set:', c['model_overrides'])
" \
&& env -u LD_LIBRARY_PATH uv run training/train.py training/configs/telugu_pilot.yaml 2>&1 | tee -a ~/SageMaker/tts/logs/pilot_train.log
wrote /home/ec2-user/SageMaker/tts/data/pilot/tokenizer.json (46 texts match sentencepiece exactly)
-rw-r--r--. 1 ec2-user ec2-user 279227 Oct 18 05:43 /home/ec2-user/SageMaker/tts/data/pilot/tokenizer.json
tokenizer path set: {'flow_lm.lookup_table.tokenizer_path': '/home/ec2-user/SageMaker/tts/data/pilot/tokenizer.json'}
[18-10 05:43:17 INFO train] logging to /home/ec2-user/SageMaker/tts/runs/telugu_pilot/logs/train_20261018-054317.log
[18-10 05:43:17 INFO train] torch 2.14.0+cu130 | cuda (NVIDIA A10G) | world size 1
[18-10 05:43:17 INFO train] resolved config from training/configs/telugu_pilot.yaml:
data:
  train_jsonl: /home/ec2-user/SageMaker/tts/data/pilot/train_aligned.jsonl
  valid_jsonl: /home/ec2-user/SageMaker/tts/data/pilot/valid_aligned.jsonl
  max_duration_sec: 30.0
  max_voice_prompt_sec: 5.0
  prompt_trim_max_sec: 0.5
  final_punct_dropout: 0.3
  shuffle: true
  loader_procs: 3
  num_bucket_batches: 5
  precompute: true
flow:
  type: lsd
  kwargs: {}
optim:
  lr: 0.0002
  weight_decay: 0.1
  betas:
  - 0.9
  - 0.95
  eps: 1.0e-08
  max_norm: 1.0
  warmup_steps: 50
  schedule: constant
  lr_min_ratio: 0.0
  type: adamw
  muon_lr: 0.005
  muon_momentum: 0.95
  muon_head: false
  muon_rms_match: false
  muon_polar_steps: 6
model_config: pocket_tts/config/english_2026-04_24l.yaml
model_overrides:
  flow_lm.lookup_table.tokenizer_path: /home/ec2-user/SageMaker/tts/data/pilot/tokenizer.json
start_from_pretrained: true
freeze_head: false
reset_text_embedding: true
run_dir: /home/ec2-user/SageMaker/tts/runs/telugu_pilot
batch_size: 16
grad_accum_steps: 4
max_steps: 200
seed: 42
flow_batch_multiplier: 4
eos_loss_weight: 0.1
text_dropout: 0.2
voice_dropout: 0.2
stats_ema_steps: 1000
stats_ema_decay: 0.999
log_freq: 50
valid_freq: 100
compile: true
num_valid_batches: 50
sample_sentences:
- The quick brown fox jumps over the lazy dog.
- Training is still running; this voice is a work in progress.
- How much wood would a woodchuck chuck if a woodchuck could chuck wood?
sample_freq: 10000
sample_temp: 0.3
sample_cfg_coef: 2.0
ckpt_freq: 200
num_ckpt_keep: 1
ema_decay: 0.999
distill_cfg_coef: 0.0
distill_teacher_config: ''
distill_teacher_overrides: {}
distill_teacher_weights: ''
distill_teacher_use_ema: true
student_init_from: ''
[18-10 05:43:17 INFO pocket_tts.modules.text_conditioner] Loading tokenizers json from /home/ec2-user/SageMaker/tts/data/pilot/tokenizer.json
[18-10 05:43:19 INFO httpx] HTTP Request: HEAD https://huggingface.co/kyutai/pocket-tts/resolve/492522650173a0653b7575cdc25ae09810e5d741/languages/english_2026-04_24l/model.safetensors "HTTP/1.1 302 Found"
[18-10 05:43:19 INFO httpx] HTTP Request: GET https://huggingface.co/api/models/kyutai/pocket-tts/xet-read-token/492522650173a0653b7575cdc25ae09810e5d741 "HTTP/1.1 200 OK"
[18-10 05:43:38 INFO training.modules.builders] starting the text embedding from scratch: ['conditioner.embed.weight']
[18-10 05:43:39 INFO train] precomputing latents for train_aligned.jsonl (one-time)
[18-10 05:43:47 INFO precompute_latents] train_aligned.jsonl: stitch_frames=35 (noise floor 0.0e+00)
encode train_aligned.jsonl: 100%|██████████| 71/71 [00:21<00:00,  3.23it/s]
[18-10 05:44:09 INFO precompute_latents] wrote /home/ec2-user/SageMaker/tts/data/pilot/train_aligned_latents.jsonl and /home/ec2-user/SageMaker/tts/data/pilot/train_aligned_latents.meta.json
[18-10 05:44:09 INFO train] flow_lm + objective: 316.0M trainable params
[18-10 05:44:22 INFO train] starting training loop, first step can take a few minutes (compilation etc.)
/home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/jit/_script.py:1491: FutureWarning: `torch.jit.script` is deprecated. Please switch to `torch.compile` or `torch.export`.
  warnings.warn(
[18-10 05:45:14 INFO train] first step took 52s, including compilation
[18-10 05:45:14 INFO train] step 1 | lr 4.00e-06 | grad 0.92 | 0.02 it/s | {'flow_diag': '21.1847', 'flow_distill': '0.2681', 'flow_loss': '0.5049', 'eos_loss': '0.1499', 'loss': '0.5199'}
[18-10 05:45:15 INFO train] step 2 | lr 8.00e-06 | grad 0.53 | 1.25 it/s | {'flow_diag': '20.6256', 'flow_loss': '0.4834', 'eos_loss': '0.0633', 'loss': '0.4897'}
[18-10 05:45:15 INFO train] step 3 | lr 1.20e-05 | grad 0.51 | 1.33 it/s | {'flow_diag': '20.4559', 'flow_loss': '0.4794', 'eos_loss': '0.0762', 'loss': '0.4871'}
[18-10 05:45:16 INFO train] step 4 | lr 1.60e-05 | grad 0.87 | 1.05 it/s | {'flow_diag': '20.3192', 'flow_loss': '0.4762', 'eos_loss': '0.1135', 'loss': '0.4876'}
[18-10 05:45:17 INFO train] step 5 | lr 2.00e-05 | grad 0.76 | 1.20 it/s | {'flow_diag': '19.7722', 'flow_loss': '0.4634', 'eos_loss': '0.0585', 'loss': '0.4693'}
[18-10 05:45:18 INFO train] step 6 | lr 2.40e-05 | grad 0.57 | 1.49 it/s | {'flow_diag': '19.3351', 'flow_loss': '0.4531', 'eos_loss': '0.0410', 'loss': '0.4572'}
[18-10 05:45:19 INFO train] step 7 | lr 2.80e-05 | grad 0.80 | 1.33 it/s | {'flow_diag': '19.3131', 'flow_distill': '0.3394', 'flow_loss': '0.4632', 'eos_loss': '0.0370', 'loss': '0.4669'}
[18-10 05:45:19 INFO train] step 8 | lr 3.20e-05 | grad 0.77 | 1.26 it/s | {'flow_diag': '19.2342', 'flow_loss': '0.4508', 'eos_loss': '0.0372', 'loss': '0.4545'}
[18-10 05:45:20 INFO train] step 9 | lr 3.60e-05 | grad 1.19 | 1.01 it/s | {'flow_diag': '18.5186', 'flow_distill': '0.3504', 'flow_loss': '0.4448', 'eos_loss': '0.0176', 'loss': '0.4466'}
[18-10 05:45:21 INFO train] step 10 | lr 4.00e-05 | grad 0.76 | 0.95 it/s | {'flow_diag': '18.2038', 'flow_loss': '0.4266', 'eos_loss': '0.0126', 'loss': '0.4279'}
[18-10 05:45:21 INFO train] per-step logging done, logging every 50 steps from now on
[18-10 05:46:02 INFO train] step 50 | lr 2.00e-04 | grad 1.03 | 0.99 it/s | {'flow_diag': '17.1662', 'flow_loss': '0.4007', 'eos_loss': '0.0039', 'loss': '0.4011'}
[18-10 05:46:44 INFO train] step 100 | lr 2.00e-04 | grad 1.02 | 1.19 it/s | {'flow_diag': '16.3407', 'flow_loss': '0.3778', 'eos_loss': '0.0092', 'loss': '0.3788'}
[18-10 05:46:44 INFO training.dataloader.manifest] indexed 37 entries from /home/ec2-user/SageMaker/tts/data/pilot/valid_aligned.jsonl (rank 0/1)
[18-10 05:47:04 INFO train] valid @ step 100: {'flow_diag': '16.6822', 'flow_distill': '0.3737', 'flow_loss': '0.3853', 'eos_loss': '0.0110', 'loss': '0.3864'}
[18-10 05:47:47 INFO train] step 150 | lr 2.00e-04 | grad 0.75 | 0.80 it/s | {'flow_diag': '15.3066', 'flow_loss': '0.3495', 'eos_loss': '0.0015', 'loss': '0.3496'}
[18-10 05:48:35 INFO train] step 200 | lr 2.00e-04 | grad 1.05 | 1.03 it/s | {'flow_diag': '15.1253', 'flow_loss': '0.3414', 'eos_loss': '0.0030', 'loss': '0.3417'}
[18-10 05:48:35 INFO training.dataloader.manifest] indexed 37 entries from /home/ec2-user/SageMaker/tts/data/pilot/valid_aligned.jsonl (rank 0/1)
[18-10 05:48:52 INFO train] valid @ step 200: {'flow_diag': '16.7778', 'flow_distill': '0.3734', 'flow_loss': '0.3759', 'eos_loss': '0.0175', 'loss': '0.3776'}
[18-10 05:48:59 INFO training.checkpointing] saved /home/ec2-user/SageMaker/tts/runs/telugu_pilot/checkpoint_00000200.pt
[18-10 05:49:08 INFO training.checkpointing] exported pocket-tts weights to /home/ec2-user/SageMaker/tts/runs/telugu_pilot/model.safetensors
[18-10 05:50:14 INFO training.checkpointing] saved /home/ec2-user/SageMaker/tts/runs/telugu_pilot/checkpoint_00000200.pt
[18-10 05:50:25 INFO training.checkpointing] exported pocket-tts weights to /home/ec2-user/SageMaker/tts/runs/telugu_pilot/model.safetensors
[18-10 05:50:25 INFO train] peak GPU memory 15.9 GiB
[18-10 05:50:25 INFO train] done
```

---

## Paste 07  (transcript user message #143, 2026-10-18T05:57:12.928Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ source ~/SageMaker/tts/env.sh && cd ~/SageMaker/tts/pocket-tts && env -u LD_LIBRARY_PATH uv run python - <<'EOF'
import os, yaml, json
h = os.path.expanduser('~/SageMaker/tts')
c = yaml.safe_load(open('pocket_tts/config/english_2026-04_24l.yaml'))
c['flow_lm']['lookup_table']['tokenizer_path'] = f'{h}/data/pilot/tokenizer.json'
yaml.safe_dump(c, open(f'{h}/runs/telugu_pilot/pilot_gen.yaml', 'w'), sort_keys=False)
r = json.loads(open(f'{h}/data/pilot/valid.jsonl').readline())
open(f'{h}/runs/telugu_pilot/gen_args.txt', 'w').write(r['path'] + '\n' + r['transcript'])
print(r)
EOF
{'path': '/home/ec2-user/SageMaker/tts/data/pilot/wavs/IISc_SYSPINProject_te_m_AGRI_02122.wav', 'duration': 9.079, 'transcript': 'వెల్లటూరు, కిష్టాపురం, అడ్లూరు, నెమలిపురి గ్రామాలకు రాకపోకలు నిలిచిపోగా గ్రామ సమీపాల్లోని పంట పొలాలు నీట మునిగాయి.'}
[ec2-user@ip-REDACTED pocket-tts]$ cd ~/SageMaker/tts/pocket-tts && R=~/SageMaker/tts/runs/telugu_pilot && env -u LD_LIBRARY_PATH uv run pocket-tts generate --config $R/pilot_gen.yaml --checkpoint $R/checkpoint_00000200.pt --voice "$(sed -n 1p $R/gen_args.txt)" --text "$(sed -n 2p $R/gen_args.txt)" --output-path $R/pilot_test.wav --device cuda 2>&1 | tail -15
INFO: Loading model from config at /home/ec2-user/SageMaker/tts/runs/telugu_pilot/pilot_gen.yaml...
INFO: Loading tokenizers json from /home/ec2-user/SageMaker/tts/data/pilot/tokenizer.json
INFO: Encoding audio prompt took 293 ms
INFO: Prompting audio took 79 ms
INFO: Size of the model state for audio prompt: 22 MB
INFO: starting timer now!
INFO: Prompting text took 28 ms
INFO: Average generation step time: 33 ms
INFO: Waiting for mimi decoder to finish took 0 ms
INFO: Generated: 1520 ms of audio in 705 ms so 2.16x faster than real-time
INFO: Results written in /home/ec2-user/SageMaker/tts/runs/telugu_pilot/pilot_test.wav
INFO: --------------------
INFO: If you want to try multiple voices and prompts quickly, try the `serve` command.
INFO: If you like Kyutai projects, comment, like, subscribe at https://x.com/kyutai_labs
[ec2-user@ip-REDACTED pocket-tts]$ python3 -c "
import wave,json,os
R=os.path.expanduser('~/SageMaker/tts/runs/telugu_pilot')
w=wave.open(R+'/pilot_test.wav'); print('generated seconds:', w.getnframes()/w.getframerate())
print('real clip seconds:', json.loads(open(os.path.expanduser('~/SageMaker/tts/data/pilot/valid.jsonl')).readline())['duration'])"
generated seconds: 1.72
real clip seconds: 9.079
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 08  (transcript user message #150, 2026-10-18T06:23:06.765Z)

```
[ec2-user@ip-REDACTED ~]$ cd ~/SageMaker/tts && cat > env.sh <<'EOF'
export UV_CACHE_DIR="$HOME/SageMaker/tts/uv-cache"
export UV_PYTHON_INSTALL_DIR="$HOME/SageMaker/tts/uv-python"
export HF_HOME="$HOME/SageMaker/tts/hf-home"
export PATH="$HOME/SageMaker/tts/bin:$PATH"
EOF
source env.sh && curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="$HOME/SageMaker/tts/bin" UV_NO_MODIFY_PATH=1 sh \
&& python3 -m venv venv_tools && venv_tools/bin/pip install -q imageio-ffmpeg \
&& ln -sf "$(venv_tools/bin/python -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')" bin/ffmpeg \
&& git clone https://github.com/kyutai-labs/pocket-tts.git && cd pocket-tts && uv sync && git rev-parse HEAD
sh: source: env.sh: file not found
[ec2-user@ip-REDACTED tts]$
```

---

## Paste 09  (transcript user message #152, 2026-10-18T06:25:19.069Z)

```
[ec2-user@ip-REDACTED ~]$ cd ~/SageMaker/tts && cat > env.sh <<'EOF'
export UV_CACHE_DIR="$HOME/SageMaker/tts/uv-cache"
export UV_PYTHON_INSTALL_DIR="$HOME/SageMaker/tts/uv-python"
export HF_HOME="$HOME/SageMaker/tts/hf-home"
export PATH="$HOME/SageMaker/tts/bin:$PATH"
EOF
source env.sh && curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="$HOME/SageMaker/tts/bin" UV_NO_MODIFY_PATH=1 sh \
&& python3 -m venv venv_tools && venv_tools/bin/pip install -q imageio-ffmpeg \
&& ln -sf "$(venv_tools/bin/python -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')" bin/ffmpeg \
&& git clone https://github.com/kyutai-labs/pocket-tts.git && cd pocket-tts && uv sync && git rev-parse HEAD
sh: source: env.sh: file not found
[ec2-user@ip-REDACTED tts]$ cd ~/SageMaker/tts && ls env.sh && source ./env.sh && curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="$HOME/SageMaker/tts/bin" UV_NO_MODIFY_PATH=1 sh \
&& python3 -m venv venv_tools && venv_tools/bin/pip install -q imageio-ffmpeg \
&& ln -sf "$(venv_tools/bin/python -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')" bin/ffmpeg \
&& git clone https://github.com/kyutai-labs/pocket-tts.git && cd pocket-tts && uv sync && git rev-parse HEAD
env.sh
downloading uv 0.13.1 x86_64-unknown-linux-gnu
installing to /home/ec2-user/SageMaker/tts/bin
  uv
  uvx
everything's installed!

[notice] A new release of pip is available: 23.0.1 -> 26.2.1
[notice] To update, run: python3 -m pip install --upgrade pip
Cloning into 'pocket-tts'...
remote: Enumerating objects: 1838, done.
remote: Counting objects: 100% (1261/1261), done.
remote: Compressing objects: 100% (660/660), done.
remote: Total 1838 (delta 986), reused 605 (delta 601), pack-reused 577 (from 3)
Receiving objects: 100% (1838/1838), 2.48 MiB | 17.66 MiB/s, done.
Resolving deltas: 100% (1134/1134), done.
Using CPython 3.10.22
Creating virtual environment at: .venv
Resolved 120 packages in 1ms
      Built pocket-tts @ file:///home/ec2-user/SageMaker/tts/pocket-tts                                                                                                                
Prepared 113 packages in 7.41s
Installed 113 packages in 350ms
 + annotated-doc==0.0.5
 + annotated-types==0.8.0
 + anyio==4.15.1
 + babel==2.18.0
 + backrefs==8.0
 + certifi==2026.7.22
 + cffi==2.1.1
 + charset-normalizer==3.5.1
 + click==8.5.0
 + colorama==0.4.6
 + coverage==7.16.1
 + cuda-bindings==13.4.1
 + cuda-pathfinder==1.8.1
 + cuda-toolkit==13.0.3.0
 + einops==0.8.2
 + exceptiongroup==1.3.1
 + execnet==2.1.2
 + fastapi==0.141.1
 + filelock==4.0.0
 + fsspec==2026.7.0
 + ghp-import==2.1.0
 + griffelib==2.3.0
 + h11==0.16.0
 + hf-xet==1.6.0
 + httpcore==1.0.9
 + httpx==0.28.1
 + huggingface-hub==1.32.0
 + idna==3.19
 + indic-numtowords==1.1.0
 + iniconfig==2.3.0
 + jinja2==3.1.6
 + jiwer==4.0.0
 + line-profiler==5.0.2
 + markdown==3.10.3
 + markdown-it-py==4.2.0
 + markupsafe==3.0.3
 + mdurl==0.1.2
 + mergedeep==1.3.4
 + mkdocs==1.6.1
 + mkdocs-autolinks-plugin==0.7.1
 + mkdocs-autorefs==1.4.4
 + mkdocs-get-deps==0.2.2
 + mkdocs-material==9.7.7
 + mkdocs-material-extensions==1.3.1
 + mkdocstrings==1.0.6
 + mkdocstrings-python==2.0.8
 + more-itertools==11.1.0
 + mpmath==1.3.0
 + networkx==3.4.2
 + numpy==2.2.6
 + nvidia-cublas==13.1.1.3
 + nvidia-cuda-cupti==13.0.85
 + nvidia-cuda-nvrtc==13.0.88
 + nvidia-cuda-runtime==13.0.96
 + nvidia-cudnn-cu13==9.24.0.43
 + nvidia-cufft==12.0.0.61
 + nvidia-cufile==1.15.1.6
 + nvidia-curand==10.4.0.35
 + nvidia-cusolver==12.0.4.66
 + nvidia-cusparse==12.6.3.3
 + nvidia-cusparselt-cu13==0.8.1
 + nvidia-nccl-cu13==2.30.7
 + nvidia-nvjitlink==13.4.92
 + nvidia-nvshmem-cu13==3.4.5
 + nvidia-nvtx==13.0.85
 + packaging==26.3
 + paginate==0.5.7
 + pathspec==1.1.1
 + platformdirs==4.11.9
 + pluggy==1.6.0
 + pocket-tts==3.3.0 (from file:///home/ec2-user/SageMaker/tts/pocket-tts)
 + pycparser==3.0
 + pydantic==2.13.5
 + pydantic-core==2.46.5
 + pygments==2.21.0
 + pymdown-extensions==12.0.1
 + pytest==9.1.1
 + pytest-xdist==3.8.0
 + python-dateutil==2.9.0.post0
 + python-multipart==0.0.32
 + pyyaml==6.0.3
 + pyyaml-env-tag==1.1
 + rapidfuzz==3.14.5
 + regex==2026.9.10
 + requests==2.34.2
 + rich==15.0.0
 + safetensors==0.8.0
 + scipy==1.15.3
 + sentencepiece==0.2.2
 + setuptools==84.0.0
 + shellingham==1.5.4
 + six==1.17.0
 + soundfile==0.14.0
 + sphn==0.2.1
 + starlette==1.6.0
 + sympy==1.14.0
 + text2num==3.1.0
 + tokenizers==0.23.2
 + tomli==2.4.1
 + torch==2.14.0
 + torchaudio==2.11.0
 + tqdm==4.70.1
 + transformers==5.17.0
 + triton==3.8.0
 + ty==0.0.81
 + typer==0.27.2
 + typing-extensions==4.16.0
 + typing-inspection==0.4.4
 + urllib3==2.8.0
 + utmos-pytorch==0.1.0
 + uvicorn==0.53.0
 + watchdog==6.0.0
 + whisper-normalizer==0.1.15
1df6b3da17cb43eff8c4c4e077f785520492adff
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 10  (transcript user message #153, 2026-10-18T06:27:50.198Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ cd ~/SageMaker/tts/pocket-tts && source ~/SageMaker/tts/env.sh && uv run hf auth login && uv run hf auth whoami
Hint: A new version of huggingface_hub (2.2.0) is available! You are using version 1.32.0.
Hint: The `hf-cli` skill is not installed. Run `hf skills add -g --claude` to teach your AI agents how to use the `hf` CLI.
? How would you like to log in? Paste an access token
    To log in, `huggingface_hub` requires a token generated from https://huggingface.co/settings/tokens .
Enter your token (input will not be visible): 
Token is valid (permission: fineGrained).
The token `[HF-TOKEN-NAME-REDACTED]` has been saved to /home/ec2-user/SageMaker/tts/hf-home/stored_tokens
Your token has been saved to /home/ec2-user/SageMaker/tts/hf-home/token
Login successful.
The current active token is: `[HF-TOKEN-NAME-REDACTED]`
✓ Logged in
  user: 10xwath
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 11  (transcript user message #155, 2026-10-18T06:28:37.304Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ cd ~/SageMaker/tts/pocket-tts && source ~/SageMaker/tts/env.sh && uv run python -c "from huggingface_hub import hf_hub_download as d; print(d('kyutai/pocket-tts','languages/english_2026-04_24l/model.safetensors'))" && pgrep -x tar | wc -l && du -sh ~/SageMaker/tts/data/raw
languages/english_2026-04_24l/model.safe(…): downloading bytes: ██████████████████████████████████████████████████████████████████████████████████████████████████|  603MB, 56.6MB/s  
languages/english_2026-04_24l/model.safe(…): reconstructing file: 100%|██████████████████████████████████████████████████████████████████████████████████| 1.30GB / 1.30GB,  121MB/s  
/home/ec2-user/SageMaker/tts/hf-home/hub/models--kyutai--pocket-tts/snapshots/79556530b8cef3f7c8f526c5c412b65c2a4c2202/languages/english_2026-04_24l/model.safetensors
0
52G     /home/ec2-user/SageMaker/tts/data/raw
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 12  (transcript user message #156, 2026-10-18T06:29:08.558Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ source ~/SageMaker/tts/env.sh && ls ~/SageMaker/tts/scripts/prep_syspin.py && ls ~/SageMaker/tts/data/raw/IISc_SYSPIN_Data/ && cd ~/SageMaker/tts/scripts && R=$HOME/SageMaker/tts/data/raw/IISc_SYSPIN_Data && for s in Male Female; do nohup python3 prep_syspin.py --root $R/IISc_SYSPINProject_Telugu_${s}_Spk001_HC --out $HOME/SageMaker/tts/data/full_$s --workers 22 > ~/SageMaker/tts/logs/prep_$s.log 2>&1 & done; sleep 5; tail -n 2 ~/SageMaker/tts/logs/prep_Male.log ~/SageMaker/tts/logs/prep_Female.log
ls: cannot access '/home/ec2-user/SageMaker/tts/scripts/prep_syspin.py': No such file or directory
tail: cannot open '/home/ec2-user/SageMaker/tts/logs/prep_Male.log' for reading: No such file or directory
tail: cannot open '/home/ec2-user/SageMaker/tts/logs/prep_Female.log' for reading: No such file or directory
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 13  (transcript user message #157, 2026-10-18T06:31:15.487Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ source ~/SageMaker/tts/env.sh && ls ~/SageMaker/tts/scripts/prep_syspin.py && ls ~/SageMaker/tts/data/raw/IISc_SYSPIN_Data/ && cd ~/SageMaker/tts/scripts && R=$HOME/SageMaker/tts/data/raw/IISc_SYSPIN_Data && for s in Male Female; do nohup python3 prep_syspin.py --root $R/IISc_SYSPINProject_Telugu_${s}_Spk001_HC --out $HOME/SageMaker/tts/data/full_$s --workers 22 > ~/SageMaker/tts/logs/prep_$s.log 2>&1 & done; sleep 5; tail -n 2 ~/SageMaker/tts/logs/prep_Male.log ~/SageMaker/tts/logs/prep_Female.log
/home/ec2-user/SageMaker/tts/scripts/prep_syspin.py
IISc_SYSPINProject_Telugu_Female_Spk001_HC  IISc_SYSPINProject_Telugu_Male_Spk001_HC
[1] 39268
[2] 39269
==> /home/ec2-user/SageMaker/tts/logs/prep_Male.log <==
nohup: ignoring input

==> /home/ec2-user/SageMaker/tts/logs/prep_Female.log <==
nohup: ignoring input
[ec2-user@ip-REDACTED scripts]$
```

---

## Paste 14  (transcript user message #158, 2026-10-18T06:33:32.913Z)

```
[ec2-user@ip-REDACTED scripts]$ tail -n 1 ~/SageMaker/tts/logs/prep_Male.log ~/SageMaker/tts/logs/prep_Female.log
==> /home/ec2-user/SageMaker/tts/logs/prep_Male.log <==
processed 352/21041  kept 339  0.75 h

==> /home/ec2-user/SageMaker/tts/logs/prep_Female.log <==
processed 352/20830  kept 345  0.87 h
[ec2-user@ip-REDACTED scripts]$
```

---

## Paste 15  (transcript user message #159, 2026-10-18T06:35:21.571Z)

```
processed 352/20830  kept 345  0.87 h
[ec2-user@ip-REDACTED scripts]$ f(){ tail -n1 ~/SageMaker/tts/logs/prep_$1.log | sed -E 's#processed ([0-9]+)/([0-9]+).*#\1 \2#'; }; a1=$(f Male | cut -d' ' -f1); b1=$(f Female | cut -d' ' -f1); sleep 60; a2=$(f Male | cut -d' ' -f1); t1=$(f Male | cut -d' ' -f2); b2=$(f Female | cut -d' ' -f1); t2=$(f Female | cut -d' ' -f2); echo "Male: $((a2-a1)) clips/min, ETA about $(( (t1-a2)/(a2-a1+1) )) min"; echo "Female: $((b2-b1)) clips/min, ETA about $(( (t2-b2)/(b2-b1+1) )) min"f(){ tail -n1 ~/SageMaker/tts/logs/prep_$1.log | sed -E 's#processed ([0-9]+)/([0-9]+).*#\1 \2#'; }; a1=$(f Male | cut -d' ' -f1); b1=$(f Female | cut -d' ' -f1); sleep 60; a2=$(f Male | cut -d' ' -f1); t1=$(f Male | cut -d' ' -f2); b2=$(f Female | cut -d' ' -f1); t2=$(f Female | cut -d' ' -f2); echo "Male: $((a2-a1)) clips/min, ETA about $(( (t1-a2)/(a2-a1+1) )) min"; echo "Female: $((b2-b1)) clips/min, ETA about $(( (t2-b2)/(b2-b1+1) )) min"
sh: syntax error near unexpected token `('
[ec2-user@ip-REDACTED scripts]$ f(){ tail -n1 ~/SageMaker/tts/logs/prep_$1.log | sed -E 's#processed ([0-9]+)/([0-9]+).*#\1 \2#'; }; a1=$(f Male | cut -d' ' -f1); b1=$(f Female | cut -d' ' -f1); sleep 60; a2=$(f Male | cut -d' ' -f1); t1=$(f Male | cut -d' ' -f2); b2=$(f Female | cut -d' ' -f1); t2=$(f Female | cut -d' ' -f2); echo "Male: $((a2-a1)) clips/min, ETA about $(( (t1-a2)/(a2-a1+1) )) min"; echo "Female: $((b2-b1)) clips/min, ETA about $(( (t2-b2)/(b2-b1+1) )) min"
Male: 352 clips/min, ETA about 55 min
Female: 352 clips/min, ETA about 55 min
[ec2-user@ip-REDACTED scripts]$
```

---

## Paste 16  (transcript user message #160, 2026-10-18T06:36:18.682Z)

```
[ec2-user@ip-REDACTED scripts]$ uptime; top -bn1 | head -12
 06:36:11 up 24 min,  0 users,  load average: 14.92, 9.46, 5.42
top - 06:36:12 up 24 min,  0 users,  load average: 14.92, 9.46, 5.42
Tasks: 651 total,   6 running, 645 sleeping,   0 stopped,   0 zombie
%Cpu(s): 32.0 us, 19.4 sy,  7.2 ni, 41.3 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem : 191168.4 total, 114604.8 free,   7371.2 used,  69192.4 buff/cache
MiB Swap:      0.0 total,      0.0 free,      0.0 used. 182063.8 avail Mem 

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
 123973 root      29   9  112380 102752   6428 R  94.1   0.1   0:23.04 systemd-coredum
 125866 root      29   9  112380 102760   6436 R  94.1   0.1   0:21.96 systemd-coredum
 128124 ec2-user  20   0  600660  51944  14272 I  94.1   0.0   0:00.43 ffmpeg
 128464 root      29   9  112380  11628   6420 R  94.1   0.0   0:00.34 systemd-coredum
 128575 ec2-user  20   0  596308  63960  13512 S  94.1   0.0   0:00.30 ffmpeg
[ec2-user@ip-REDACTED scripts]$
```

---

## Paste 17  (transcript user message #161, 2026-10-18T06:43:59.307Z)

```
[ec2-user@ip-REDACTED scripts]$ n0=$(sudo coredumpctl list --no-pager 2>/dev/null | grep -vc ffmpeg); (ulimit -c 1; sh -c 'kill -SEGV $$'); sleep 4; n1=$(sudo coredumpctl list --no-pager 2>/dev/null | grep -vc ffmpeg); if [ "$n1" = "$n0" ]; then echo "TRICK WORKS: restarting prep"; pkill -f prep_syspin.py; pkill -x ffmpeg; sleep 3; ulimit -c 1; source ~/SageMaker/tts/env.sh; cd ~/SageMaker/tts/scripts; R=$HOME/SageMaker/tts/data/raw/IISc_SYSPIN_Data; for s in Male Female; do nohup python3 prep_syspin.py --root $R/IISc_SYSPINProject_Telugu_${s}_Spk001_HC --out $HOME/SageMaker/tts/data/full_$s --workers 22 > ~/SageMaker/tts/logs/prep_$s.log 2>&1 & done; sleep 5; echo restarted; else echo "TRICK DOES NOT WORK: leave prep running"; fi
Segmentation fault (core dumped)
TRICK DOES NOT WORK: leave prep running
[ec2-user@ip-REDACTED scripts]$
```

---

## Paste 18  (transcript user message #169, 2026-10-18T07:18:39.856Z)

```
[ec2-user@ip-REDACTED scripts]$ pgrep -f prep_syspin.py > /dev/null && echo "still running" || echo "finished"; tail -n 1 ~/SageMaker/tts/logs/prep_Male.log ~/SageMaker/tts/logs/prep_Female.log
still running
==> /home/ec2-user/SageMaker/tts/logs/prep_Male.log <==
processed 16544/21041  kept 15921  35.13 h

==> /home/ec2-user/SageMaker/tts/logs/prep_Female.log <==
processed 17600/20830  kept 17335  43.39 h
[ec2-user@ip-REDACTED scripts]$
```

---

## Paste 19  (transcript user message #171, 2026-10-18T07:21:15.327Z)

```
can we parallelly download rasa and keep the ongoing download going as well?


[ec2-user@ip-REDACTED scripts]$ cd ~/SageMaker/tts/pocket-tts && source ~/SageMaker/tts/env.sh && uv run python -c "
from huggingface_hub import list_repo_tree
for f in list_repo_tree('ai4bharat/Rasa', repo_type='dataset', recursive=True):
    print(getattr(f,'size',None), f.path)" > ~/SageMaker/tts/logs/rasa_tree.txt 2>&1; wc -l ~/SageMaker/tts/logs/rasa_tree.txt; head -25 ~/SageMaker/tts/logs/rasa_tree.txt; echo ---; grep -i -E "telugu|/te[/_.-]|_te[/_.-]" ~/SageMaker/tts/logs/rasa_tree.txt | head -30
1341 /home/ec2-user/SageMaker/tts/logs/rasa_tree.txt
None Assamese
None Bengali
None Bodo
None Dogri
None Gujarati
None Hindi
None Kannada
None Kashmiri
None Konkani
None Maithili
None Malayalam
None Manipuri
None Marathi
None Nepali
None Odia
None Punjabi
None Sanskrit
None Santali
None Sindhi
None Tamil
None Telugu
None Urdu
2461 .gitattributes
258255926 Assamese/test-00000-of-00007.parquet
262404972 Assamese/test-00001-of-00007.parquet
---
None Telugu
240410197 Telugu/test-00000-of-00007.parquet
239231408 Telugu/test-00001-of-00007.parquet
240582013 Telugu/test-00002-of-00007.parquet
248272110 Telugu/test-00003-of-00007.parquet
235585641 Telugu/test-00004-of-00007.parquet
237559343 Telugu/test-00005-of-00007.parquet
239079410 Telugu/test-00006-of-00007.parquet
279757226 Telugu/train-00000-of-00056.parquet
258344650 Telugu/train-00001-of-00056.parquet
281323205 Telugu/train-00002-of-00056.parquet
277172994 Telugu/train-00003-of-00056.parquet
280867094 Telugu/train-00004-of-00056.parquet
273530184 Telugu/train-00005-of-00056.parquet
273650213 Telugu/train-00006-of-00056.parquet
273850495 Telugu/train-00007-of-00056.parquet
260259849 Telugu/train-00008-of-00056.parquet
267639866 Telugu/train-00009-of-00056.parquet
272258501 Telugu/train-00010-of-00056.parquet
276604296 Telugu/train-00011-of-00056.parquet
265062971 Telugu/train-00012-of-00056.parquet
271239406 Telugu/train-00013-of-00056.parquet
275589982 Telugu/train-00014-of-00056.parquet
264775002 Telugu/train-00015-of-00056.parquet
268049418 Telugu/train-00016-of-00056.parquet
262734339 Telugu/train-00017-of-00056.parquet
264160334 Telugu/train-00018-of-00056.parquet
271510023 Telugu/train-00019-of-00056.parquet
261637553 Telugu/train-00020-of-00056.parquet
286263235 Telugu/train-00021-of-00056.parquet
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 20  (transcript user message #172, 2026-10-18T07:22:46.105Z)

```
52G     /home/ec2-user/SageMaker/tts/data/raw
[ec2-user@ip-REDACTED pocket-tts]$ source ~/SageMaker/tts/env.sh && ls ~/SageMaker/tts/scripts/prep_syspin.py && ls ~/SageMaker/tts/data/raw/IISc_SYSPIN_Data/ && cd ~/SageMaker/tts/scripts && R=$HOME/SageMaker/tts/data/raw/IISc_SYSPIN_Data && for s in Male Female; do nohup python3 prep_syspin.py --root $R/IISc_SYSPINProject_Telugu_${s}_Spk001_HC --out $HOME/SageMaker/tts/data/full_$s --workers 22 > ~/SageMaker/tts/logs/prep_$s.log 2>&1 & done; sleep 5; tail -n 2 ~/SageMaker/tts/logs/prep_Male.log ~/SageMaker/tts/logs/prep_Female.log
ls: cannot access '/home/ec2-user/SageMaker/tts/scripts/prep_syspin.py': No such file or directory
tail: cannot open '/home/ec2-user/SageMaker/tts/logs/prep_Male.log' for reading: No such file or directory
tail: cannot open '/home/ec2-user/SageMaker/tts/logs/prep_Female.log' for reading: No such file or directory
[ec2-user@ip-REDACTED pocket-tts]$ ls -la ~/SageMaker/tts/scripts/ ~/SageMaker/tts/eval/
ls: cannot access '/home/ec2-user/SageMaker/tts/eval/': No such file or directory
/home/ec2-user/SageMaker/tts/scripts/:
total 20
drwxr-xr-x.  2 ec2-user ec2-user 4096 Oct 18 06:30 .
drwxr-xr-x. 12 ec2-user ec2-user 4096 Oct 18 06:26 ..
-rw-r--r--.  1 ec2-user ec2-user 7361 Oct 18 06:30 prep_syspin.py
-rw-r--r--.  1 ec2-user ec2-user 1439 Oct 18 06:30 sync_to_s3.sh
[ec2-user@ip-REDACTED pocket-tts]$ source ~/SageMaker/tts/env.sh && ls ~/SageMaker/tts/scripts/prep_syspin.py && ls ~/SageMaker/tts/data/raw/IISc_SYSPIN_Data/ && cd ~/SageMaker/tts/scripts && R=$HOME/SageMaker/tts/data/raw/IISc_SYSPIN_Data && for s in Male Female; do nohup python3 prep_syspin.py --root $R/IISc_SYSPINProject_Telugu_${s}_Spk001_HC --out $HOME/SageMaker/tts/data/full_$s --workers 22 > ~/SageMaker/tts/logs/prep_$s.log 2>&1 & done; sleep 5; tail -n 2 ~/SageMaker/tts/logs/prep_Male.log ~/SageMaker/tts/logs/prep_Female.log
/home/ec2-user/SageMaker/tts/scripts/prep_syspin.py
IISc_SYSPINProject_Telugu_Female_Spk001_HC  IISc_SYSPINProject_Telugu_Male_Spk001_HC
[1] 39268
[2] 39269
==> /home/ec2-user/SageMaker/tts/logs/prep_Male.log <==
nohup: ignoring input

==> /home/ec2-user/SageMaker/tts/logs/prep_Female.log <==
nohup: ignoring input
[ec2-user@ip-REDACTED scripts]$ tail -n 1 ~/SageMaker/tts/logs/prep_Male.log ~/SageMaker/tts/logs/prep_Female.log
==> /home/ec2-user/SageMaker/tts/logs/prep_Male.log <==
processed 352/21041  kept 339  0.75 h

==> /home/ec2-user/SageMaker/tts/logs/prep_Female.log <==
processed 352/20830  kept 345  0.87 h
[ec2-user@ip-REDACTED scripts]$ f(){ tail -n1 ~/SageMaker/tts/logs/prep_$1.log | sed -E 's#processed ([0-9]+)/([0-9]+).*#\1 \2#'; }; a1=$(f Male | cut -d' ' -f1); b1=$(f Female | cut -d' ' -f1); sleep 60; a2=$(f Male | cut -d' ' -f1); t1=$(f Male | cut -d' ' -f2); b2=$(f Female | cut -d' ' -f1); t2=$(f Female | cut -d' ' -f2); echo "Male: $((a2-a1)) clips/min, ETA about $(( (t1-a2)/(a2-a1+1) )) min"; echo "Female: $((b2-b1)) clips/min, ETA about $(( (t2-b2)/(b2-b1+1) )) min"f(){ tail -n1 ~/SageMaker/tts/logs/prep_$1.log | sed -E 's#processed ([0-9]+)/([0-9]+).*#\1 \2#'; }; a1=$(f Male | cut -d' ' -f1); b1=$(f Female | cut -d' ' -f1); sleep 60; a2=$(f Male | cut -d' ' -f1); t1=$(f Male | cut -d' ' -f2); b2=$(f Female | cut -d' ' -f1); t2=$(f Female | cut -d' ' -f2); echo "Male: $((a2-a1)) clips/min, ETA about $(( (t1-a2)/(a2-a1+1) )) min"; echo "Female: $((b2-b1)) clips/min, ETA about $(( (t2-b2)/(b2-b1+1) )) min"
sh: syntax error near unexpected token `('
[ec2-user@ip-REDACTED scripts]$ f(){ tail -n1 ~/SageMaker/tts/logs/prep_$1.log | sed -E 's#processed ([0-9]+)/([0-9]+).*#\1 \2#'; }; a1=$(f Male | cut -d' ' -f1); b1=$(f Female | cut -d' ' -f1); sleep 60; a2=$(f Male | cut -d' ' -f1); t1=$(f Male | cut -d' ' -f2); b2=$(f Female | cut -d' ' -f1); t2=$(f Female | cut -d' ' -f2); echo "Male: $((a2-a1)) clips/min, ETA about $(( (t1-a2)/(a2-a1+1) )) min"; echo "Female: $((b2-b1)) clips/min, ETA about $(( (t2-b2)/(b2-b1+1) )) min"
Male: 352 clips/min, ETA about 55 min
Female: 352 clips/min, ETA about 55 min
[ec2-user@ip-REDACTED scripts]$ uptime; top -bn1 | head -12
 06:36:11 up 24 min,  0 users,  load average: 14.92, 9.46, 5.42
top - 06:36:12 up 24 min,  0 users,  load average: 14.92, 9.46, 5.42
Tasks: 651 total,   6 running, 645 sleeping,   0 stopped,   0 zombie
%Cpu(s): 32.0 us, 19.4 sy,  7.2 ni, 41.3 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem : 191168.4 total, 114604.8 free,   7371.2 used,  69192.4 buff/cache
MiB Swap:      0.0 total,      0.0 free,      0.0 used. 182063.8 avail Mem 

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
 123973 root      29   9  112380 102752   6428 R  94.1   0.1   0:23.04 systemd-coredum
 125866 root      29   9  112380 102760   6436 R  94.1   0.1   0:21.96 systemd-coredum
 128124 ec2-user  20   0  600660  51944  14272 I  94.1   0.0   0:00.43 ffmpeg
 128464 root      29   9  112380  11628   6420 R  94.1   0.0   0:00.34 systemd-coredum
 128575 ec2-user  20   0  596308  63960  13512 S  94.1   0.0   0:00.30 ffmpeg
[ec2-user@ip-REDACTED scripts]$ n0=$(sudo coredumpctl list --no-pager 2>/dev/null | grep -vc ffmpeg); (ulimit -c 1; sh -c 'kill -SEGV $$'); sleep 4; n1=$(sudo coredumpctl list --no-pager 2>/dev/null | grep -vc ffmpeg); if [ "$n1" = "$n0" ]; then echo "TRICK WORKS: restarting prep"; pkill -f prep_syspin.py; pkill -x ffmpeg; sleep 3; ulimit -c 1; source ~/SageMaker/tts/env.sh; cd ~/SageMaker/tts/scripts; R=$HOME/SageMaker/tts/data/raw/IISc_SYSPIN_Data; for s in Male Female; do nohup python3 prep_syspin.py --root $R/IISc_SYSPINProject_Telugu_${s}_Spk001_HC --out $HOME/SageMaker/tts/data/full_$s --workers 22 > ~/SageMaker/tts/logs/prep_$s.log 2>&1 & done; sleep 5; echo restarted; else echo "TRICK DOES NOT WORK: leave prep running"; fi
Segmentation fault (core dumped)
TRICK DOES NOT WORK: leave prep running
[ec2-user@ip-REDACTED scripts]$ pgrep -f prep_syspin.py > /dev/null && echo "still running" || echo "finished"; tail -n 1 ~/SageMaker/tts/logs/prep_Male.log ~/SageMaker/tts/logs/prep_Female.log
still running
==> /home/ec2-user/SageMaker/tts/logs/prep_Male.log <==
processed 16544/21041  kept 15921  35.13 h

==> /home/ec2-user/SageMaker/tts/logs/prep_Female.log <==
processed 17600/20830  kept 17335  43.39 h
[ec2-user@ip-REDACTED scripts]$ cd ~/SageMaker/tts/pocket-tts && source ~/SageMaker/tts/env.sh && uv run python -c "
from huggingface_hub import list_repo_tree
for f in list_repo_tree('ai4bharat/Rasa', repo_type='dataset', recursive=True):
    print(getattr(f,'size',None), f.path)" > ~/SageMaker/tts/logs/rasa_tree.txt 2>&1; wc -l ~/SageMaker/tts/logs/rasa_tree.txt; head -25 ~/SageMaker/tts/logs/rasa_tree.txt; echo ---; grep -i -E "telugu|/te[/_.-]|_te[/_.-]" ~/SageMaker/tts/logs/rasa_tree.txt | head -30
1341 /home/ec2-user/SageMaker/tts/logs/rasa_tree.txt
None Assamese
None Bengali
None Bodo
None Dogri
None Gujarati
None Hindi
None Kannada
None Kashmiri
None Konkani
None Maithili
None Malayalam
None Manipuri
None Marathi
None Nepali
None Odia
None Punjabi
None Sanskrit
None Santali
None Sindhi
None Tamil
None Telugu
None Urdu
2461 .gitattributes
258255926 Assamese/test-00000-of-00007.parquet
262404972 Assamese/test-00001-of-00007.parquet
---
None Telugu
240410197 Telugu/test-00000-of-00007.parquet
239231408 Telugu/test-00001-of-00007.parquet
240582013 Telugu/test-00002-of-00007.parquet
248272110 Telugu/test-00003-of-00007.parquet
235585641 Telugu/test-00004-of-00007.parquet
237559343 Telugu/test-00005-of-00007.parquet
239079410 Telugu/test-00006-of-00007.parquet
279757226 Telugu/train-00000-of-00056.parquet
258344650 Telugu/train-00001-of-00056.parquet
281323205 Telugu/train-00002-of-00056.parquet
277172994 Telugu/train-00003-of-00056.parquet
280867094 Telugu/train-00004-of-00056.parquet
273530184 Telugu/train-00005-of-00056.parquet
273650213 Telugu/train-00006-of-00056.parquet
273850495 Telugu/train-00007-of-00056.parquet
260259849 Telugu/train-00008-of-00056.parquet
267639866 Telugu/train-00009-of-00056.parquet
272258501 Telugu/train-00010-of-00056.parquet
276604296 Telugu/train-00011-of-00056.parquet
265062971 Telugu/train-00012-of-00056.parquet
271239406 Telugu/train-00013-of-00056.parquet
275589982 Telugu/train-00014-of-00056.parquet
264775002 Telugu/train-00015-of-00056.parquet
268049418 Telugu/train-00016-of-00056.parquet
262734339 Telugu/train-00017-of-00056.parquet
264160334 Telugu/train-00018-of-00056.parquet
271510023 Telugu/train-00019-of-00056.parquet
261637553 Telugu/train-00020-of-00056.parquet
286263235 Telugu/train-00021-of-00056.parquet
[ec2-user@ip-REDACTED pocket-tts]$ cd ~/SageMaker/tts/pocket-tts && source ~/SageMaker/tts/env.sh && mkdir -p ~/SageMaker/tts/data/rasa && nohup uv run hf download ai4bharat/Rasa --repo-type dataset --include "Telugu/*" --local-dir ~/SageMaker/tts/data/rasa > ~/SageMaker/tts/logs/rasa_dl.log 2>&1 & sleep 5; tail -c 300 ~/SageMaker/tts/logs/rasa_dl.log
[3] 840624
k on /home/ec2-user/SageMaker/tts/data/rasa/.cache/huggingface/.gitignore.lock (elapsed: 0.1 seconds)
Still waiting to acquire lock on /home/ec2-user/SageMaker/tts/data/rasa/.cache/huggingface/.gitignore.lock (elapsed: 0.1 seconds)
Fetching 63 files:   2%|▏         | 1/63 [00:02<02:16,  2.20s/it][ec2-user@ip-REDACTED pocket-tts]$ du -sh ~/SageMaker/tts/data/rasa; pgrep -f "hf download" > /dev/null && echo downloading || echo finished             du -sh ~/SageMaker/tts/data/rasa; pgrep -f "hf download" > /dev/null && echo downloading || echo finished
4.0G    /home/ec2-user/SageMaker/tts/data/rasa
downloading
[ec2-user@ip-REDACTED pocket-tts]$ cd ~/SageMaker/tts/pocket-tts && source ~/SageMaker/tts/env.sh && uv run --with pyarrow python -c "
import pyarrow.parquet as pq, glob
p = sorted(glob.glob('$HOME/SageMaker/tts/data/rasa/Telugu/train-*.parquet'))[0]
f = pq.ParquetFile(p); print(f.schema_arrow); print('rows in this shard:', f.metadata.num_rows)
t = f.read_row_group(0).slice(0, 2).to_pylist()
for r in t: print({k: (v if k != 'audio' else {kk: (vv if kk != 'bytes' else str(len(vv)) + ' bytes') for kk, vv in v.items()}) for k, v in r.items()})"
Installed 1 package in 28ms
filename: string
text: string
language: string
gender: string
style: string
duration: string
wav_path: string
audio: struct<bytes: binary, path: string>
  child 0, bytes: binary
  child 1, path: string
-- schema metadata --
huggingface: '{"info": {"features": {"filename": {"dtype": "string", "_ty' + 342
rows in this shard: 489
{'filename': 'TEL_F_WIKI_01212', 'text': 'ఏదేమైనా, పొగచూరిన పంది మాంసాన్ని పులియబెట్టిన సోయాబీన్తో వండిన వంటకం ఈ రాష్ట్ర వంటకం.', 'language': 'Telugu', 'gender': 'Female', 'style': 'WIKI', 'duration': '6.578', 'wav_path': '/data/TTS/ttsteam/datasets/rasa_hf/data_20251203/Telugu/Female/wavs/TEL_F_WIKI_01212.wav', 'audio': {'bytes': '631532 bytes', 'path': 'TEL_F_WIKI_01212.wav'}}
{'filename': 'TEL_F_WIKI_01359', 'text': 'అంటే మీకు అన్ని కూడా భోజనం, మధ్యాహ్నం భోజనం పథకాలని అమ్మఒడి వసతి దివేన ఇలాంటివన్నీ పడుతున్నాయి కదండి, విద్య దీవెన గవర్నమెంట్ నుంచి మంచి ఫ్యాకల్టీ కూడా ఉందండి, టీచర్లు కూడా మంచి వాళ్లు బాగా చెప్తారు.', 'language': 'Telugu', 'gender': 'Female', 'style': 'WIKI', 'duration': '14.655', 'wav_path': '/data/TTS/ttsteam/datasets/rasa_hf/data_20251203/Telugu/Female/wavs/TEL_F_WIKI_01359.wav', 'audio': {'bytes': '1406924 bytes', 'path': 'TEL_F_WIKI_01359.wav'}}
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 21  (transcript user message #173, 2026-10-18T08:03:18.404Z)

```
ec2-user@ip-REDACTED pocket-tts]$ nohup bash ~/SageMaker/tts/scripts/run_pipeline.sh > ~/SageMaker/tts/logs/pipeline.out 2>&1 &
[4] 927847
[ec2-user@ip-REDACTED pocket-tts]$ sleep 3; cat ~/SageMaker/tts/logs/pipeline.log
07:27:17 pipeline started
07:27:17 Rasa download finished, parquet files: 63 (expected 63)
07:27:17 Rasa prep started (pid 919877)
07:27:22 pipeline started
07:27:22 Rasa download finished, parquet files: 63 (expected 63)
07:27:22 Rasa prep started (pid 928128)
[ec2-user@ip-REDACTED pocket-tts]$ tail -n 25 ~/SageMaker/tts/logs/pipeline.log
07:27:17 pipeline started
07:27:17 Rasa download finished, parquet files: 63 (expected 63)
07:27:17 Rasa prep started (pid 919877)
07:27:22 pipeline started
07:27:22 Rasa download finished, parquet files: 63 (expected 63)
07:27:22 Rasa prep started (pid 928128)
07:32:53 SYSPIN prep finished
07:33:03 SYSPIN prep finished
07:41:12 Rasa prep finished
07:41:12 combined: 68402 train, 1395 valid
hours kept Male: 44.543
hours kept Female: 51.406
hours kept Rasa: 49.399
hours kept TOTAL: 145.3
07:41:12 alignment of train started on 4 GPUs
07:41:44 Rasa prep finished
07:41:44 combined: 68402 train, 1395 valid
hours kept Male: 44.543
hours kept Female: 51.406
hours kept Rasa: 49.399
hours kept TOTAL: 145.3
07:41:44 alignment of train started on 4 GPUs
07:50:04 FAILED at stage: alignment of a train part (see logs/align_*.log). Pipeline stopped. Nothing after this stage ran.
07:52:20 aligned: train 33382 of 68402, valid 1395
07:52:20 FAILED at stage: alignment lost more than 5% of train clips (33382 of 68402). Pipeline stopped. Nothing after this stage ran.
[1]   Done                    nohup python3 prep_syspin.py --root $R/IISc_SYSPINProject_Telugu_${s}_Spk001_HC --out $HOME/SageMaker/tts/data/full_$s --workers 22 > ~/SageMaker/tts/logs/prep_$s.log 2>&1  (wd: ~/SageMaker/tts/scripts)
(wd now: ~/SageMaker/tts/pocket-tts)
[3]-  Done(1)                 nohup bash ~/SageMaker/tts/scripts/run_pipeline.sh > ~/SageMaker/tts/logs/pipeline.out 2>&1
[4]+  Done(1)                 nohup bash ~/SageMaker/tts/scripts/run_pipeline.sh > ~/SageMaker/tts/logs/pipeline.out 2>&1
[ec2-user@ip-REDACTED pocket-tts]$


 

also i hope we have maximum gpu utilization
```

---

## Paste 22  (transcript user message #174, 2026-10-18T08:05:25.492Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ pgrep -af "run_pipeline|align_data|prep_" | grep -v pgrep | head; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv; for i in 0 1 2 3; do echo "== align_$i"; tr '\r' '\n' < ~/SageMaker/tts/logs/align_$i.log | grep -v '^align:' | tail -5; done; ls ~/SageMaker/tts/logs/pipeline.lock 2>&1 | head -1
index, memory.used [MiB], utilization.gpu [%]
0, 0 MiB, 0 %
1, 0 MiB, 0 %
2, 0 MiB, 0 %
3, 0 MiB, 0 %
== align_0
[W1018 07:49:39.953822961 CUDACachingAllocator.cpp:3934] memory allocation failed with OOM on device 0 while trying to allocate 2944401408 bytes (free: 979435520, total: 23686938624).

  full_bar = Bar(frac,

[18-10 07:50:03 INFO align] done: 15539 aligned, 0 skipped
== align_1
OutOfMemoryError: CUDA out of memory. Tried to allocate 2.47 GiB. GPU 0 has a total capacity of 22.06 GiB of which 1.25 GiB is free. Process 2178913 has 13.96 GiB memory in use. 
Including non-PyTorch memory, this process has 6.83 GiB memory in use. Of the allocated memory 5.66 GiB is allocated by PyTorch, and 897.02 MiB is reserved by PyTorch but unallocated.
If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  
(https://docs.pytorch.org/docs/stable/notes/cuda.html#optimizing-memory-usage-with-pytorch-cuda-alloc-conf)

== align_2
[W1018 07:51:27.095589002 CUDACachingAllocator.cpp:3934] memory allocation failed with OOM on device 0 while trying to allocate 4261412864 bytes (free: 1340211200, total: 23686938624).

  full_bar = Bar(frac,

[18-10 07:51:35 INFO align] done: 17331 aligned, 0 skipped
== align_3
OutOfMemoryError: CUDA out of memory. Tried to allocate 2.60 GiB. GPU 0 has a total capacity of 22.06 GiB of which 2.49 GiB is free. Process 2178941 has 13.00 GiB memory in use. 
Including non-PyTorch memory, this process has 6.56 GiB memory in use. Of the allocated memory 5.93 GiB is allocated by PyTorch, and 331.97 MiB is reserved by PyTorch but unallocated.
If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  
(https://docs.pytorch.org/docs/stable/notes/cuda.html#optimizing-memory-usage-with-pytorch-cuda-alloc-conf)

ls: cannot access '/home/ec2-user/SageMaker/tts/logs/pipeline.lock': No such file or directory
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 23  (transcript user message #175, 2026-10-18T08:06:59.220Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ grep -c "pipeline.lock" ~/SageMaker/tts/scripts/run_pipeline.sh
3
[ec2-user@ip-REDACTED pocket-tts]$ FRESH_RASA=1 nohup bash ~/SageMaker/tts/scripts/run_pipeline.sh > ~/SageMaker/tts/logs/pipeline.out 2>&1 &
[1] 2188990
[ec2-user@ip-REDACTED pocket-tts]$ tail -n 8 ~/SageMaker/tts/logs/pipeline.log
07:50:04 FAILED at stage: alignment of a train part (see logs/align_*.log). Pipeline stopped. Nothing after this stage ran.
07:52:20 aligned: train 33382 of 68402, valid 1395
07:52:20 FAILED at stage: alignment lost more than 5% of train clips (33382 of 68402). Pipeline stopped. Nothing after this stage ran.
08:06:35 pipeline started
08:06:35 FRESH_RASA=1: deleting data/full_Rasa
08:06:37 Rasa download finished, parquet files: 63 (expected 63)
08:06:37 Rasa prep started (pid 2189010)
08:06:37 SYSPIN prep finished
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 24  (transcript user message #177, 2026-10-18T08:42:09.159Z)

```
ec2-user@ip-REDACTED pocket-tts]$ tail -n 25 ~/SageMaker/tts/logs/pipeline.log
07:50:04 FAILED at stage: alignment of a train part (see logs/align_*.log). Pipeline stopped. Nothing after this stage ran.
07:52:20 aligned: train 33382 of 68402, valid 1395
07:52:20 FAILED at stage: alignment lost more than 5% of train clips (33382 of 68402). Pipeline stopped. Nothing after this stage ran.
08:06:35 pipeline started
08:06:35 FRESH_RASA=1: deleting data/full_Rasa
08:06:37 Rasa download finished, parquet files: 63 (expected 63)
08:06:37 Rasa prep started (pid 2189010)
08:06:37 SYSPIN prep finished
08:18:53 Rasa prep finished
08:18:53 combined: 68402 train, 1395 valid
hours kept Male: 44.543
hours kept Female: 51.406
hours kept Rasa: 49.399
hours kept TOTAL: 145.3
08:18:53 alignment of train started on 4 GPUs
08:26:53 aligned: train 68402 of 68402, valid 1395
wrote /home/ec2-user/SageMaker/tts/data/full/tokenizer.json (1404 texts match sentencepiece exactly)
08:27:05 tokenizer done
config keys set: ['batch_size', 'ckpt_freq', 'grad_accum_steps', 'max_steps', 'num_ckpt_keep', 'run_dir', 'train_jsonl', 'valid_freq', 'valid_jsonl']
NOT FOUND: ['sample_freq', 'sample_sentences']
sample sentences: 3
Traceback (most recent call last):
  File "<stdin>", line 24, in <module>
AssertionError: some config keys were not found
08:27:05 FAILED at stage: config. Pipeline stopped. Nothing after this stage ran.
[1]+  Done(1)                 FRESH_RASA=1 nohup bash ~/SageMaker/tts/scripts/run_pipeline.sh > ~/SageMaker/tts/logs/pipeline.out 2>&1
[ec2-user@ip-REDACTED pocket-tts]$ c
```

---

## Paste 25  (transcript user message #178, 2026-10-18T08:43:50.407Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ source ~/SageMaker/tts/env.sh && cd ~/SageMaker/tts/pocket-tts && env -u LD_LIBRARY_PATH uv run python - <<'EOF'
import json, os, yaml
h = os.path.expanduser('~/SageMaker/tts')
c = yaml.safe_load(open('training/configs/finetune_language.yaml'))
samples = []
for line in open(f'{h}/data/full/valid.jsonl', encoding='utf-8'):
    t = json.loads(line)['transcript']
    if 40 <= len(t) <= 90 and not any(ch.isdigit() for ch in t):
        samples.append(t)
    if len(samples) == 3:
        break
ov = {
  'train_jsonl': f'{h}/data/full/train_aligned.jsonl', 'valid_jsonl': f'{h}/data/full/valid_aligned.jsonl',
  'run_dir': f'{h}/runs/telugu_full', 'batch_size': 16, 'grad_accum_steps': 1, 'max_steps': 15000,
  'valid_freq': 2500, 'ckpt_freq': 2500, 'num_ckpt_keep': 3,
}
hit = set()
def walk(d):
    for k, v in d.items():
        if k in ov: d[k] = ov[k]; hit.add(k)
        elif isinstance(v, dict): walk(v)
walk(c)
assert not (set(ov) - hit), set(ov) - hit
c['sample_freq'] = 2500
c['sample_sentences'] = samples
c['model_overrides']['flow_lm.lookup_table.tokenizer_path'] = f'{h}/data/full/tokenizer.json'
yaml.safe_dump(c, open('training/configs/telugu_full.yaml', 'w'), sort_keys=False, allow_unicode=True)
print('written. samples:', len(samples)); print({k: c[k] for k in ('batch_size','grad_accum_steps','max_steps','valid_freq','ckpt_freq','num_ckpt_keep','sample_freq','run_dir')})
print(c['model_overrides'])
EOF
written. samples: 3
{'batch_size': 16, 'grad_accum_steps': 1, 'max_steps': 15000, 'valid_freq': 2500, 'ckpt_freq': 2500, 'num_ckpt_keep': 3, 'sample_freq': 2500, 'run_dir': '/home/ec2-user/SageMaker/tts/runs/telugu_full'}
{'flow_lm.lookup_table.tokenizer_path': '/home/ec2-user/SageMaker/tts/data/full/tokenizer.json'}
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 26  (transcript user message #179, 2026-10-18T08:47:54.614Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ source ~/SageMaker/tts/env.sh && cd ~/SageMaker/tts/pocket-tts && nohup env -u LD_LIBRARY_PATH uv run torchrun --nproc-per-node 4 training/train.py training/configs/telugu_full.yaml > ~/SageMaker/tts/logs/full_train.log 2>&1 &
[1] 2814409
[ec2-user@ip-REDACTED pocket-tts]$ sleep 15; grep -m4 -E "world size|torch|Error|Traceback" ~/SageMaker/tts/logs/full_train.log
W1018 08:44:20.111000 2814413 torch/distributed/run.py:982] 
W1018 08:44:20.111000 2814413 torch/distributed/run.py:982] *****************************************
W1018 08:44:20.111000 2814413 torch/distributed/run.py:982] Setting OMP_NUM_THREADS environment variable for each process to be 1 in default, to avoid your system being overloaded, please further tune the variable for optimal performance in your application as needed. 
W1018 08:44:20.111000 2814413 torch/distributed/run.py:982] *****************************************
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 27  (transcript user message #180, 2026-10-18T08:48:40.191Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ BUCKET=aarav-10x RUN_DIR=$HOME/SageMaker/tts/runs/telugu_full RUN_NAME=telugu_full nohup bash ~/SageMaker/tts/scripts/sync_to_s3.sh > ~/SageMaker/tts/logs/sync.log 2>&1 &
[2] 2815827
[1]   Done(1)                 source ~/SageMaker/tts/env.sh && cd ~/SageMaker/tts/pocket-tts && nohup env -u LD_LIBRARY_PATH uv run torchrun --nproc-per-node 4 training/train.py training/configs/telugu_full.yaml > ~/SageMaker/tts/logs/full_train.log 2>&1
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 28  (transcript user message #181, 2026-10-18T08:52:13.115Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ tail -n 40 ~/SageMaker/tts/logs/full_train.log | cut -c1-220
  File "/home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/distributed/launcher/api.py", line 197, in __call__
    return launch_agent(
  File "/home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/distributed/launcher/api.py", line 386, in launch_agent
    raise ChildFailedError(
torch.distributed.elastic.multiprocessing.errors.ChildFailedError: 
============================================================
training/train.py FAILED
------------------------------------------------------------
Failures:
[1]:
  time      : 2026-10-18_08:47:48
  host      : ip-REDACTED.ec2.internal
  rank      : 0 (local_rank: 0)
  exitcode  : -15 (pid: 2814482)  (SIGTERM)
  error_file: <N/A>
  traceback : Signal 15 (SIGTERM) received by PID 2814482
[2]:
  time      : 2026-10-18_08:47:48
  host      : ip-REDACTED.ec2.internal
  rank      : 1 (local_rank: 1)
  exitcode  : -15 (pid: 2814483)  (SIGTERM)
  error_file: <N/A>
  traceback : Signal 15 (SIGTERM) received by PID 2814483
[3]:
  time      : 2026-10-18_08:47:48
  host      : ip-REDACTED.ec2.internal
  rank      : 2 (local_rank: 2)
  exitcode  : -15 (pid: 2814484)  (SIGTERM)
  error_file: <N/A>
  traceback : Signal 15 (SIGTERM) received by PID 2814484
------------------------------------------------------------
Root Cause (first observed failure):
[0]:
  time      : 2026-10-18_08:47:48
  host      : ip-REDACTED.ec2.internal
  rank      : 3 (local_rank: 3)
  exitcode  : 1 (pid: 2814485) 
  error_file: <N/A>
  traceback : To enable traceback see: https://pytorch.org/docs/stable/elastic/errors.html
============================================================
[ec2-user@ip-REDACTED pocket-tts]$ nvidia-smi --query-gpu=index,memory.used --format=csv; ls ~/SageMaker/tts/runs/telugu_full 2>&1 | head
index, memory.used [MiB]
0, 0 MiB
1, 0 MiB
2, 0 MiB
3, 0 MiB
args.yaml
logs
progress.jsonl
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 29  (transcript user message #183, 2026-10-18T08:54:25.084Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ f=~/SageMaker/tts/logs/full_train.log; n=$(grep -n -m1 "Traceback (most recent" $f | cut -d: -f1); echo "first traceback at line: $n"; sed -n "$((n>12 ? n-12 : 1)),$((n+30))p" $f | cut -c1-200
first traceback at line: 121
[18-10 08:44:29 INFO train] precomputing latents for train_aligned.jsonl (one-time)
encode train_aligned.jsonl:   0%|          | 0/535 [00:00<?, ?it/s]
encode train_aligned.jsonl:   0%|          | 3/534 [00:19<44:55,  5.08s/it]  
[rank0]:[W1018 08:47:33.638737397 CUDACachingAllocator.cpp:528] expandable_segments: memory mapping failed with OOM on device 0 while trying to map 20971520 bytes (free: 16121856, total: 23686938624).
encode train_aligned.jsonl: 100%|█████████▉| 533/535 [03:02<00:02,  1.01s/it][rank0]:[W1018 08:47:34.832324982 CUDACachingAllocator.cpp:528] expandable_segments: memory mapping failed with OOM on dev
[rank0]:[W1018 08:47:34.031215604 CUDACachingAllocator.cpp:528] expandable_segments: memory mapping failed with OOM on device 0 while trying to map 20971520 bytes (free: 14024704, total: 23686938624).
encode train_aligned.jsonl: 100%|██████████| 534/534 [03:02<00:00,  2.92it/s]
encode train_aligned.jsonl: 100%|██████████| 534/534 [03:03<00:00,  2.91it/s]
encode train_aligned.jsonl: 100%|██████████| 535/535 [02:44<00:00,  1.56s/it]
encode train_aligned.jsonl: 100%|██████████| 535/535 [03:04<00:00,  2.90it/s]
[18-10 08:47:41 INFO precompute_latents] wrote /home/ec2-user/SageMaker/tts/data/full/train_aligned_latents.jsonl and /home/ec2-user/SageMaker/tts/data/full/train_aligned_latents.meta.json
[18-10 08:47:41 INFO train] flow_lm + objective: 316.0M trainable params
[rank3]: Traceback (most recent call last):
[rank3]:   File "/home/ec2-user/SageMaker/tts/pocket-tts/training/train.py", line 380, in <module>
[rank3]:     main(sys.argv[1])
[rank3]:   File "/home/ec2-user/SageMaker/tts/pocket-tts/training/train.py", line 167, in main
[rank3]:     run = setup(config_path)
[rank3]:   File "/home/ec2-user/SageMaker/tts/pocket-tts/training/train.py", line 147, in setup
[rank3]:     wrapped = DDP(model, device_ids=[device.index], find_unused_parameters=not args.compile)
[rank3]:   File "/home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/nn/parallel/distributed.py", line 1064, in __init__
[rank3]:     _verify_param_shape_across_processes(self.process_group, parameters)
[rank3]:   File "/home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/distributed/utils.py", line 299, in _verify_param_shape_across_processes
[rank3]:     return dist._verify_params_across_processes(process_group, tensors, logger)
[rank3]: torch.distributed.DistBackendError: NCCL error in: /__w/pytorch/pytorch/torch/csrc/distributed/c10d/ProcessGroupNCCL.cpp:3888, unhandled cuda error (run with NCCL_DEBUG=INFO for details), NCC
[rank3]: ncclUnhandledCudaError: Call to CUDA function failed.
[rank3]: Last error:
[rank3]: Cuda failure 2 'out of memory'
W1018 08:47:48.225000 2814413 torch/distributed/elastic/multiprocessing/api.py:1028] Sending process 2814482 closing signal SIGTERM
W1018 08:47:48.226000 2814413 torch/distributed/elastic/multiprocessing/api.py:1028] Sending process 2814483 closing signal SIGTERM
W1018 08:47:48.226000 2814413 torch/distributed/elastic/multiprocessing/api.py:1028] Sending process 2814484 closing signal SIGTERM
E1018 08:47:48.955000 2814413 torch/distributed/elastic/multiprocessing/api.py:1002] failed (exitcode: 1) local_rank: 3 (pid: 2814485) of binary: /home/ec2-user/SageMaker/tts/pocket-tts/.venv/bin/pyth
Traceback (most recent call last):
  File "/home/ec2-user/SageMaker/tts/pocket-tts/.venv/bin/torchrun", line 10, in <module>
    sys.exit(main())
  File "/home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/distributed/elastic/multiprocessing/errors/__init__.py", line 380, in wrapper
    return f(*args, **kwargs)
  File "/home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/distributed/run.py", line 1138, in main
    run(args)
  File "/home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/distributed/run.py", line 1129, in run
    elastic_launch(
  File "/home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/distributed/launcher/api.py", line 197, in __call__
    return launch_agent(
  File "/home/ec2-user/SageMaker/tts/pocket-tts/.venv/lib/python3.10/site-packages/torch/distributed/launcher/api.py", line 386, in launch_agent
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 30  (transcript user message #184, 2026-10-18T08:57:59.996Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ source ~/SageMaker/tts/env.sh && cd ~/SageMaker/tts/pocket-tts && nohup env -u LD_LIBRARY_PATH uv run torchrun --nproc-per-node 4 training/train.py training/configs/telugu_full.yaml > ~/SageMaker/tts/logs/full_train.log 2>&1 &
[3] 2817494
[ec2-user@ip-REDACTED pocket-tts]$ grep -E "world size|precomput|latents|first step|step [0-9]+ \||Error|Traceback" ~/SageMaker/tts/logs/full_train.log | tail -8 | cut -c1-200
[18-10 08:56:51 INFO train] step 3 | lr 6.00e-07 | grad 1.38 | 0.11 it/s | {'flow_diag': '21.0376', 'flow_distill': '0.2929', 'flow_loss': '0.5022', 'eos_loss': '0.1300', 'loss': '0.5152'}
[18-10 08:56:52 INFO train] step 4 | lr 8.00e-07 | grad 1.33 | 1.38 it/s | {'flow_diag': '20.8342', 'flow_distill': '0.3042', 'flow_loss': '0.4978', 'eos_loss': '0.0631', 'loss': '0.5041'}
[18-10 08:56:52 INFO train] step 5 | lr 1.00e-06 | grad 0.53 | 1.86 it/s | {'flow_diag': '21.9313', 'flow_loss': '0.5140', 'eos_loss': '0.0854', 'loss': '0.5226'}
[18-10 08:56:53 INFO train] step 6 | lr 1.20e-06 | grad 0.53 | 1.77 it/s | {'flow_diag': '20.7773', 'flow_loss': '0.4870', 'eos_loss': '0.1643', 'loss': '0.5034'}
[18-10 08:56:53 INFO train] step 7 | lr 1.40e-06 | grad 0.49 | 1.86 it/s | {'flow_diag': '20.4560', 'flow_loss': '0.4794', 'eos_loss': '0.0800', 'loss': '0.4874'}
[18-10 08:56:54 INFO train] step 8 | lr 1.60e-06 | grad 0.52 | 1.85 it/s | {'flow_diag': '20.9659', 'flow_loss': '0.4914', 'eos_loss': '0.0520', 'loss': '0.4966'}
[18-10 08:57:01 INFO train] step 9 | lr 1.80e-06 | grad 0.53 | 0.14 it/s | {'flow_diag': '22.4276', 'flow_loss': '0.5256', 'eos_loss': '0.1241', 'loss': '0.5381'}
[18-10 08:57:02 INFO train] step 10 | lr 2.00e-06 | grad 0.49 | 1.79 it/s | {'flow_diag': '21.2010', 'flow_loss': '0.4969', 'eos_loss': '0.0734', 'loss': '0.5042'}
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 31  (transcript user message #185, 2026-10-18T08:59:21.781Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv -l 2 -c 5
ERROR: Option --query-gpu=index,utilization.gpu,memory.used is not recognized. Please run 'nvidia-smi -h' for help.

[ec2-user@ip-REDACTED pocket-tts]$ top -bn1 | head -14; grep -E "step (50|100|150|200) \|" ~/SageMaker/tts/logs/full_train.log | cut -c1-110
top - 08:59:13 up  2:47,  0 users,  load average: 4.32, 4.00, 4.89
Tasks: 683 total,   4 running, 679 sleeping,   0 stopped,   0 zombie
%Cpu(s):  8.1 us,  0.3 sy,  0.0 ni, 91.5 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem : 191168.4 total,  81118.3 free,  29172.9 used,  80877.2 buff/cache
MiB Swap:      0.0 total,      0.0 free,      0.0 used. 159619.8 avail Mem 

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
2817569 ec2-user  20   0  118.7g   2.6g 728064 R 100.0   1.4   3:32.29 python
2817567 ec2-user  20   0  118.7g   2.6g 727736 R  94.1   1.4   3:32.46 python
2817568 ec2-user  20   0  118.7g   2.6g 728040 R  94.1   1.4   3:32.48 python
2817570 ec2-user  20   0  118.7g   2.6g 728852 S  94.1   1.4   3:32.60 python
2820371 ec2-user  20   0  224608   4220   2912 R  11.8   0.0   0:00.04 top
  33192 ec2-user  20   0 1130728 182644  21580 S   5.9   0.1   0:24.68 jupyter-nbclass
2817498 ec2-user  20   0   21.8g 535180 235960 S   5.9   0.3   0:06.52 pt_elastic
[18-10 08:57:56 INFO train] step 50 | lr 1.00e-05 | grad 0.47 | 0.73 it/s | {'flow_diag': '19.7542', 'flow_los
[18-10 08:58:38 INFO train] step 100 | lr 2.00e-05 | grad 1.37 | 1.20 it/s | {'flow_diag': '19.2195', 'flow_di
[18-10 08:59:07 INFO train] step 150 | lr 3.00e-05 | grad 1.38 | 1.72 it/s | {'flow_diag': '17.9041', 'flow_di
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 32  (transcript user message #188, 2026-10-18T09:04:34.354Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ grep -E "step [0-9]+ \|" ~/SageMaker/tts/logs/full_train.log | tail -2 | cut -c1-90
[18-10 09:03:31 INFO train] step 600 | lr 1.20e-04 | grad 0.65 | 1.72 it/s | {'flow_diag':
[18-10 09:04:00 INFO train] step 650 | lr 1.30e-04 | grad 0.65 | 1.72 it/s | {'flow_diag':
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 33  (transcript user message #189, 2026-10-18T09:07:25.300Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ for i in 1 2 3 4 5; do nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader; echo --; sleep 2; done
0, 91 %, 17377 MiB
1, 81 %, 18315 MiB
2, 87 %, 18817 MiB
3, 91 %, 18245 MiB
--
0, 100 %, 17377 MiB
1, 100 %, 18315 MiB
2, 100 %, 18817 MiB
3, 100 %, 18245 MiB
--
0, 93 %, 17377 MiB
1, 96 %, 18315 MiB
2, 100 %, 18817 MiB
3, 100 %, 18245 MiB
--
0, 100 %, 17377 MiB
1, 100 %, 18315 MiB
2, 100 %, 18817 MiB
3, 100 %, 18245 MiB
--
0, 92 %, 17377 MiB
1, 93 %, 18315 MiB
2, 91 %, 18817 MiB
3, 90 %, 18245 MiB
--
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 34  (transcript user message #203, 2026-10-18T14:49:52.969Z)

```
[ec2-user@ip-REDACTED tts]$ cd ~/SageMaker/tts/data/full && python3 -c "
import json
T=[json.loads(l) for l in open('train_aligned.jsonl')]; V=[json.loads(l) for l in open('valid_aligned.jsonl')]
tp={r['path'] for r in T}; vp={r['path'] for r in V}
tt={r['transcript'] for r in T}; vt=[r['transcript'] for r in V]
print('train', len(T), 'valid', len(V))
print('clip overlap (same file in both):', len(tp & vp))
print('valid clips whose exact text also appears in train:', sum(1 for t in vt if t in tt), 'of', len(vt))"
train 68402 valid 1395
clip overlap (same file in both): 0
valid clips whose exact text also appears in train: 222 of 1395


step 4 results
```

---

## Paste 35  (transcript user message #204, 2026-10-18T14:51:19.508Z)

```
[ec2-user@ip-REDACTED full]$ grep -c "include-seen" ~/SageMaker/tts/scripts/eval_telugu.py
1
[ec2-user@ip-REDACTED full]$
```

---

## Paste 36  (transcript user message #206, 2026-10-18T15:06:06.997Z)

```
[ec2-user@ip-REDACTED scripts]$ ls -la ~/SageMaker/tts/runs/telugu_full/eval_smoke/ 2>&1 | head; echo ---; pgrep -af "pocket-tts|eval_telugu" | cut -c1-140; echo ---; top -bn1 | head -12; echo ---; du -sh ~/SageMaker/tts/hf-home 2>/dev/null
total 616
drwxr-xr-x. 2 ec2-user ec2-user   4096 Oct 18 15:05 .
drwxr-xr-x. 5 ec2-user ec2-user   4096 Oct 18 14:52 ..
-rw-r--r--. 1 ec2-user ec2-user   1284 Oct 18 14:52 gen.yaml
-rw-r--r--. 1 ec2-user ec2-user   1915 Oct 18 15:05 results.json
-rw-r--r--. 1 ec2-user ec2-user 347564 Oct 18 15:03 valid_00.wav
-rw-r--r--. 1 ec2-user ec2-user 263084 Oct 18 15:03 valid_01.wav
---
37327 uv run python /home/ec2-user/SageMaker/tts/scripts/eval_telugu.py --checkpoint /home/ec2-user/SageMaker/tts/runs/telugu_full/checkpoin
37362 /home/ec2-user/SageMaker/tts/pocket-tts/.venv/bin/python /home/ec2-user/SageMaker/tts/scripts/eval_telugu.py --checkpoint /home/ec2-us
---
top - 15:05:59 up 25 min,  0 users,  load average: 5.21, 2.89, 1.71
Tasks: 554 total,   2 running, 552 sleeping,   0 stopped,   0 zombie
%Cpu(s):  2.0 us,  0.2 sy,  0.0 ni, 97.7 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem : 191168.4 total, 179302.9 free,   4580.4 used,   7285.1 buff/cache
MiB Swap:      0.0 total,      0.0 free,      0.0 used. 184897.1 avail Mem 

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
  37362 ec2-user  20   0   25.8g   2.0g   1.5g R 100.0   1.1   0:43.22 python
  40798 ec2-user  20   0  224476   4056   2912 R   6.2   0.0   0:00.02 top
      1 root      20   0  173840  18272  10940 S   0.0   0.0   0:02.22 systemd
      2 root      20   0       0      0      0 S   0.0   0.0   0:00.01 kthreadd
      3 root      20   0       0      0      0 S   0.0   0.0   0:00.00 pool_workqueue_release
---
3.6G    /home/ec2-user/SageMaker/tts/hf-home
[ec2-user@ip-REDACTED scripts]$
```

---

## Paste 37  (transcript user message #207, 2026-10-18T15:07:42.046Z)

```
[ec2-user@ip-REDACTED full]$ source ~/SageMaker/tts/env.sh && cd ~/SageMaker/tts/pocket-tts && uv run python ~/SageMaker/tts/scripts/eval_telugu.py --checkpoint ~/SageMaker/tts/runs/telugu_full/checkpoint_00015000.pt --n-valid 2 --out ~/SageMaker/tts/runs/telugu_full/eval_smoke 2>&1 | tail -15 | cut -c1-200
validation clips with text NOT seen in training: 979 of 1395
generating 2 clips on cpu with 8 workers ...
generated 2 of 2; failed 0
loading recogniser ...
Loading weights: 100%|██████████| 424/424 [00:00<00:00, 19795.90it/s]
valid    CER gen 0.19 | real 0.16 | length ratio 0.89 | valid_00.wav
valid    CER gen 0.09 | real 0.06 | length ratio 0.95 | valid_01.wav

===== SUMMARY (checkpoint: checkpoint_00015000.pt ) =====
VALID clips (2): CER real recordings 0.112 | CER generated 0.144 | mean length ratio gen/real 0.92 | clips under 0.5x length 0
wavs and results.json in /home/ec2-user/SageMaker/tts/runs/telugu_full/eval_smoke
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 38  (transcript user message #208, 2026-10-18T15:08:01.819Z)

```
[ec2-user@ip-REDACTED scripts]$ cd ~/SageMaker/tts/pocket-tts && source ~/SageMaker/tts/env.sh && R=$HOME/SageMaker/tts/runs/telugu_full && V=$(python3 -c "import json;print(json.loads(open('$HOME/SageMaker/tts/data/full/valid.jsonl').readline())['path'])") && s=$(date +%s) && uv run pocket-tts generate --config $R/eval_smoke/gen.yaml --checkpoint $R/checkpoint_00015000.pt --voice "$V" --text "$(sed -n 19p ~/SageMaker/tts/eval/telugu_test_sentences.txt)" --output-path $R/eval_smoke/timing.wav --device cpu 2>&1 | tail -6 | cut -c1-160; echo "this call took $(( $(date +%s) - s )) seconds"
INFO: Waiting for mimi decoder to finish took 0 ms
INFO: Generated: 2800 ms of audio in 3273 ms so 0.86x faster than real-time
INFO: Results written in /home/ec2-user/SageMaker/tts/runs/telugu_full/eval_smoke/timing.wav
INFO: --------------------
INFO: If you want to try multiple voices and prompts quickly, try the `serve` command.
INFO: If you like Kyutai projects, comment, like, subscribe at https://x.com/kyutai_labs
this call took 14 seconds
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 39  (transcript user message #210, 2026-10-18T15:09:09.348Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ tail -n 4 ~/SageMaker/tts/logs/eval_run.log | cut -c1-200
nohup: ignoring input
validation clips with text NOT seen in training: 979 of 1395
sentence voices: ['/home/ec2-user/SageMaker/tts/data/full_Male/wavs/IISc_SYSPINProject_te_m_BOOK_10500.wav', '/home/ec2-user/SageMaker/tts/data/full_Female/wavs/IISc_SYSPINProject_te_f_AGRI_00216.wav'
generating 64 clips on cpu with 8 workers ...
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 40  (transcript user message #211, 2026-10-18T15:15:01.802Z)

```
ec2-user@ip-REDACTED pocket-tts]$ tail -n 5 ~/SageMaker/tts/logs/eval_run.log | cut -c1-200
SENTENCES (40 clips): CER generated 0.117 | mean length 3.9 s
wavs and results.json in /home/ec2-user/SageMaker/tts/runs/telugu_full/eval_15000
validation clips with text NOT seen in training: 979 of 1395
sentence voices: ['/home/ec2-user/SageMaker/tts/data/full_Male/wavs/IISc_SYSPINProject_te_m_BOOK_10500.wav', '/home/ec2-user/SageMaker/tts/data/full_Female/wavs/IISc_SYSPINProject_te_f_AGRI_00216.wav'
generating 64 clips on cpu with 8 workers ...
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 41  (transcript user message #212, 2026-10-18T15:15:30.824Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ python3 -c "
import json
r=json.load(open('$HOME/SageMaker/tts/runs/telugu_full/eval_15000/results.json'))
r.sort(key=lambda x:-x['cer_generated'])
for x in r[:6]: print(round(x['cer_generated'],2), x['kind'], x['gen_seconds'], 's', x['wav'].split('/')[-1], '|', x['text'][:60], '=>', x['hyp_generated'][:60])" 2>&1 | head -12
0.3 sentence 3.16 s sent_02_v0.wav | హైదరాబాద్ తెలంగాణ రాష్ట్ర రాజధాని => అయిదురబ తెలంగాన రాష్ట్వ రాజధాని
0.26 valid 24.12 s valid_15.wav | త్వరలోనే ధనధవుడి వ్రణం నయమయిపోయింది అతను లేచిన రోజునే యుద్ధర => త్వరనం నయుమయిపోయిందిఅతను లేచిన రోజనే యుద్దరెంధానికి బైగుదేరి
0.24 valid 3.48 s valid_07.wav | ఉదాహరణకు ఒక ట్యాంకును ఊహించుకోండి => ఉదాహరణకు ఒకటాన్కును ఈహించుకొండిఈ
0.24 sentence 2.6 s sent_19_v0.wav | ధన్యవాదాలు మళ్ళీ కలుద్దాం => దన్నివాదాలు మళ్ళి కదుద్దం
0.23 valid 18.68 s valid_17.wav | ఆంధ్రప్రదేశ్లోని శ్రీకాకుళం జిల్లాలో కరోనా వైరస్ లక్షణాలున్న => ఆంధ్ర ప్రదేషలోని స్రీకాపునం జిల్లాలో కరోనవైదం చేందుకు ఏరిపాట
0.22 sentence 2.44 s sent_15_v0.wav | ఈ సినిమా నాకు చాలా నచ్చింది => ఈ సినిమనా కుచ్చాలా నర్చింది
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 42  (transcript user message #213, 2026-10-18T15:16:25.831Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ grep -E "SUMMARY|VALID clips|SENTENCES" ~/SageMaker/tts/logs/eval_run.log | cut -c1-300
===== SUMMARY (checkpoint: checkpoint_00015000.pt ) =====
VALID clips (24): CER real recordings 0.138 | CER generated 0.153 | mean length ratio gen/real 1.04 | clips under 0.5x length 0
SENTENCES (40 clips): CER generated 0.117 | mean length 3.9 s
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 43  (transcript user message #215, 2026-10-18T15:18:02.519Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ grep -E "SUMMARY|VALID clips|SENTENCES" ~/SageMaker/tts/logs/eval_run.log | cut -c1-300
===== SUMMARY (checkpoint: checkpoint_00015000.pt ) =====
VALID clips (24): CER real recordings 0.138 | CER generated 0.153 | mean length ratio gen/real 1.04 | clips under 0.5x length 0
SENTENCES (40 clips): CER generated 0.117 | mean length 3.9 s
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 44  (transcript user message #216, 2026-10-18T15:18:22.883Z)

```
SENTENCES (40 clips): CER generated 0.117 | mean length 3.9 s
[ec2-user@ip-REDACTED pocket-tts]$ tail -n 3 ~/SageMaker/tts/logs/eval_run.log | cut -c1-200; pgrep -af eval_telugu | head -1 | cut -c1-80
validation clips with text NOT seen in training: 979 of 1395
sentence voices: ['/home/ec2-user/SageMaker/tts/data/full_Male/wavs/IISc_SYSPINProject_te_m_BOOK_10500.wav', '/home/ec2-user/SageMaker/tts/data/full_Female/wavs/IISc_SYSPINProject_te_f_AGRI_00216.wav'
generating 64 clips on cpu with 8 workers ...
41393 sh -c for s in 15000 10000; do uv run python $HOME/SageMaker/tts/scripts/e
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 45  (transcript user message #218, 2026-10-18T15:25:24.787Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ grep -E "SUMMARY|VALID clips|SENTENCES" ~/SageMaker/tts/logs/eval_run.log | cut -c1-300
===== SUMMARY (checkpoint: checkpoint_00015000.pt ) =====
VALID clips (24): CER real recordings 0.138 | CER generated 0.153 | mean length ratio gen/real 1.04 | clips under 0.5x length 0
SENTENCES (40 clips): CER generated 0.117 | mean length 3.9 s
===== SUMMARY (checkpoint: checkpoint_00010000.pt ) =====
VALID clips (24): CER real recordings 0.138 | CER generated 0.153 | mean length ratio gen/real 1.05 | clips under 0.5x length 0
SENTENCES (40 clips): CER generated 0.102 | mean length 3.8 s
[1]+  Done                    source ~/SageMaker/tts/env.sh && cd ~/SageMaker/tts/pocket-tts && nohup sh -c 'for s in 15000 10000; do uv run python $HOME/SageMaker/tts/scripts/eval_telugu.py --checkpoint $HOME/SageMaker/tts/runs/telugu_full/checkpoint_000$s.pt --sentences $HOME/SageMaker/tts/eval/telugu_test_sentences.txt --out $HOME/SageMaker/tts/runs/telugu_full/eval_$s; done' > $HOME/SageMaker/tts/logs/eval_run.log 2>&1
[ec2-user@ip-REDACTED pocket-tts]$
```

---

## Paste 46  (transcript user message #219, 2026-10-18T15:26:48.389Z)

```
[ec2-user@ip-REDACTED pocket-tts]$ python3 -c "
import json,os
L=lambda s: {os.path.basename(x['wav']): x['hyp_generated'] for x in json.load(open(os.path.expanduser(f'~/SageMaker/tts/runs/telugu_full/eval_{s}/results.json')))}
a,b=L(15000),L(10000); d=sum(1 for k in a if a[k]!=b[k]); print('transcripts that differ between 15k and 10k:', d, 'of', len(a))"
transcripts that differ between 15k and 10k: 58 of 64
[ec2-user@ip-REDACTED pocket-tts]$
```
