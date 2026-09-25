# NABEEL staging certificate

`docs/scripts/nabeel-staging-certify.py` is the fail-closed machine-readable release gate for the local NABEEL chain.

It requires Chiaki and OBS binaries **and running sessions**, the NABEEL OBS profile/scene, running MediaMTX and Owncast containers, healthy Owncast HTTP readback, and at least one local NABEEL recording. It never enables production/live publishing.

A failed certificate is useful evidence: its JSON identifies the exact missing runtime gates. PAS-267 is Verified/Complete only after this certificate passes during the authorized PlayStation→Chiaki→OBS→MediaMTX→Owncast staging session and the preserved recording is reviewed.
