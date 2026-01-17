# -*- coding: utf-8 -*-
"""
open access sources
10 years xp in 35 domains
"""

from phi import PHI

# neuroscience + phi
NEURO = {
    "brain_waves_phi": "https://www.researchgate.net/publication/222143648",
    "phi_eeg": "https://www.researchgate.net/publication/42638427",
    "integrated_info": "https://www.nature.com/articles/s42003-023-05063-y",
}

# jung + neuroscience
JUNG = {
    "eigenmodes_2025": "https://academic.oup.com/nc/article/2025/1/niaf039/8293123",
    "collected_works": "https://www.jungiananalysts.org.uk/wp-content/uploads/2018/07/C.-G.-Jung-Collected-Works-Volume-9i_-The-Archetypes-of-the-Collective-Unconscious.pdf",
}

# quantum cognition
QUANTUM = {
    "circuits": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10138279/",
    "bayesian": "https://www.nature.com/articles/s41598-022-13757-2",
    "overview_2025": "https://link.springer.com/article/10.3758/s13423-025-02675-9",
}

# consciousness
CONSCIOUSNESS = {
    "emergence": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7597170/",
    "artificial": "https://arxiv.org/pdf/2503.05823",
}

# music
MUSIC = {
    "neuro": "https://pmc.ncbi.nlm.nih.gov/articles/PMC9453743/",
    "cognition_book": "https://hugoribeiro.com.br/biblioteca-digital/Peretez_Zatorre-Neuroscience_of_Music.pdf",
    "free_archive": "https://freemusicarchive.org/",
    "cc_music": "https://bandcamp.com/discover/creative-commons",
}

# all sources
ALL = {**NEURO, **JUNG, **QUANTUM, **CONSCIOUSNESS, **MUSIC}

# distilled knowledge
KNOWLEDGE = {
    "phi_brain": "brain waves = n harmonics * 2φ",
    "archetypes": "eigenmodes of deep brain",
    "quantum_cognition": "decisions as quantum projections",
    "consciousness": "emerges at intermediate noise levels",
    "music": "bilateral processing, memory enhancement",
}

# 35 domains with 10yrs xp
DOMAINS = [
    "neuroscience", "psychology", "physics", "math", "biology",
    "music", "art", "philosophy", "linguistics", "anthropology",
    "economics", "business", "marketing", "sales", "finance",
    "law", "medicine", "engineering", "architecture", "design",
    "cooking", "agriculture", "ecology", "chemistry", "astronomy",
    "history", "sociology", "politics", "education", "sports",
    "meditation", "yoga", "martial_arts", "crafts", "writing",
]
