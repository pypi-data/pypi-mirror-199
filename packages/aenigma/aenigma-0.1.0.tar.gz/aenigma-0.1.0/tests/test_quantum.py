import unittest
from aenigma import analyzer

class TestQuantum(unittest.TestCase):
    def test_quantum(self):
        analyzer.initialize_nltk()
        sample = "The intricacies of quantum mechanics have confounded scientists and theorists alike since its inception. The wave-particle duality of quantum objects, the uncertainty principle, and the observer effect have challenged our understanding of reality at its most fundamental level. From Schrödinger's cat to entanglement, the implications of quantum mechanics reach far beyond the microscopic world, with potential applications in cryptography, computing, and communication. However, as we delve deeper into the quantum realm, we must abandon our classical intuitions and embrace the counterintuitive nature of this field. It is a world where particles can exist in multiple states simultaneously, where the act of measurement can change the outcome of an experiment, and where the concept of causality becomes blurred. Only by constantly challenging our assumptions and embracing the unknown can we hope to unravel the mysteries of the quantum universe."
        expected = [
            (
                'The intricacies of quantum mechanics have confounded scientists and theorists alike since its inception.', 
                0.44
            ),
            (
                'The wave-particle duality of quantum objects, the uncertainty principle, and the observer effect have challenged our understanding of reality at its most fundamental level.',
                0.76
            ),
            (
                "From Schrödinger's cat to entanglement, the implications of quantum mechanics reach far beyond the microscopic world, with potential applications in cryptography, computing, and communication.",
                0.65
            ),
            (
                'However, as we delve deeper into the quantum realm, we must abandon our classical intuitions and embrace the counterintuitive nature of this field.',
                0.37
            ),
            (
                'It is a world where particles can exist in multiple states simultaneously, where the act of measurement can change the outcome of an experiment, and where the concept of causality becomes blurred.',
                0.52
            ),
            (
                'Only by constantly challenging our assumptions and embracing the unknown can we hope to unravel the mysteries of the quantum universe.',
                0.25
            )
            ]

        self.assertEqual(analyzer.generate_rcs_list(sample), expected)

unittest.main()