"""
ChronoGen: The Chrono-Entropic Analysis Engine
Version: 1.0.0 (Release Year 2026)
Author: Sayan Deep Bera

Description:
A computational framework for quantifying genomic plasticity using 
fractional calculus and thermodynamic entropy metrics.
"""

import numpy as np
import pandas as pd
from scipy.special import binom

class ChronoGen:
    def __init__(self, name="Generic_Experiment"):
        self.name = name
        self.alpha = None
        self.efficiency = None
        print(f"🌱 ChronoGen v1.0 initialized for: {self.name}")

    def compute_entropy(self, signal_vector):
        """Calculates Von Neumann Entropy of a gene state vector."""
        norm = np.linalg.norm(signal_vector)
        if norm == 0: return 0.0
        
        psi = signal_vector / norm
        probs = np.abs(psi)**2
        probs = probs[probs > 1e-15] # Filter noise
        
        return -np.sum(probs * np.log2(probs))

    def measure_memory(self, time_series_entropy):
        """
        Estimates the Fractional Memory Exponent (Alpha) 
        using the Grunwald-Letnikov roughness metric.
        """
        alphas = np.linspace(0.1, 1.1, 50)
        scores = []
        signal = np.array(time_series_entropy)
        
        for a in alphas:
            deriv = np.zeros(len(signal))
            for t in range(len(signal)):
                for k in range(t + 1):
                    deriv[t] += (-1)**k * binom(a, k) * signal[t - k]
            # Variance of the derivative serves as a 'smoothness' score
            scores.append(np.var(deriv[5:])) 
            
        self.alpha = alphas[np.argmin(scores)]
        return self.alpha

    def generate_report(self):
        if self.alpha is None:
            return "Error: Run measure_memory() first."
            
        return {
            "Dataset": self.name,
            "Memory_Alpha": round(self.alpha, 4),
            "Criticality": "Pole_Proximity" if abs(self.alpha - 1.0) < 0.05 else "Stable"
        }
