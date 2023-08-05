Feature: G expansion

  Scenario Outline:

    Given the allele as <Allele>
    When expanding to WHO then reducing to the <Level> level
    Then the expanded allele is found to be <Expanded Alleles>

    Examples:
      | Allele         | Level | Expanded Alleles |
      | DPB1*28:01:01G | exon  | DPB1*28:01/DPB1*296:01 |
      | C*12:02:01G    | exon  | C*12:02:01/C*12:02:02/C*12:02:03/C*12:02:04/C*12:02:05/C*12:02:06/C*12:02:07/C*12:02:08/C*12:02:09/C*12:02:10/C*12:02:11/C*12:02:12/C*12:02:13/C*12:02:14/C*12:02:15/C*12:02:16/C*12:02:17/C*12:02:18/C*12:02:19/C*12:02:20/C*12:02:21/C*12:02:22/C*12:02:23/C*12:02:24/C*12:02:25/C*12:02:26/C*12:02:27/C*12:02:28/C*12:02:29/C*12:02:30/C*12:02:31/C*12:02:32/C*12:02:33/C*12:02:34/C*12:02:35/C*12:02:36/C*12:02:37/C*12:02:38/C*12:02:39/C*12:02:40/C*12:02:41/C*12:02:42/C*12:228/C*12:234/C*12:243/C*12:261/C*12:280/C*12:281/C*12:285/C*12:303/C*12:304/C*12:307/C*12:336/C*12:338 |
