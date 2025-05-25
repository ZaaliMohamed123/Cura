import re
from difflib import get_close_matches

class MedicineAutocomplete:
    def __init__(self, medicines):
        self.medicines = medicines
        self.medicine_set = set(medicines)
        self.prefix_tree = self.build_prefix_tree(medicines)

    def build_prefix_tree(self, medicines):
        prefix_tree = {}
        for medicine in medicines:
            medicine_lower = medicine.lower()
            current_node = prefix_tree
            for char in medicine_lower:
                if char not in current_node:
                    current_node[char] = {}
                current_node = current_node[char]
            current_node['$'] = medicine  # End of word marker
        return prefix_tree

    def prefix_match(self, query):
        query_lower = query.lower()
        current_node = self.prefix_tree
        for char in query_lower:
            if char not in current_node:
                return []
            current_node = current_node[char]
        # Collect all words with the given prefix
        matches = []
        stack = [current_node]
        while stack:
            node = stack.pop()
            for key, value in node.items():
                if key == '$':
                    matches.append(value)
                else:
                    stack.append(value)
        return matches

    def substring_match(self, query):
        query_lower = query.lower()
        return [medicine for medicine in self.medicine_set if query_lower in medicine.lower()]

    def autocomplete(self, query):
        query = query.strip()
        if not query:
            return []

        # First, find prefix matches
        prefix_matches = self.prefix_match(query)
        if len(prefix_matches) >= 10:
            return prefix_matches[:10]

        # Then, find substring matches
        substring_matches = self.substring_match(query)
        substring_matches = [med for med in substring_matches if med not in prefix_matches]

        # Combine prefix and substring matches
        combined_matches = prefix_matches + substring_matches[:10 - len(prefix_matches)]

        # If we still don't have enough matches, use fuzzy matching
        if len(combined_matches) < 10:
            fuzzy_matches = get_close_matches(query, self.medicines, n=10, cutoff=0.6)
            fuzzy_matches = [match for match in fuzzy_matches if match not in combined_matches]
            combined_matches += fuzzy_matches[:10 - len(combined_matches)]

        return combined_matches[:10]

