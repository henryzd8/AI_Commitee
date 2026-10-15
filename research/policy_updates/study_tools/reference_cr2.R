# Optional independent cross-check with the authors' implementation.
# Install clubSandwich separately; no packages are installed by this script.
# Input CSV: value,family_id (one paired, model/channel-averaged difference/item).
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1) stop("Usage: Rscript reference_cr2.R paired.csv")
if (!requireNamespace("clubSandwich", quietly = TRUE)) stop("clubSandwich is required")
d <- read.csv(args[1])
fit <- lm(value ~ 1, data = d)
print(clubSandwich::coef_test(fit, vcov = "CR2", cluster = d$family_id,
                            test = "Satterthwaite"))
