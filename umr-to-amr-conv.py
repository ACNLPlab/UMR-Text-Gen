import re

'''This class contains all the methods needed to convert UMR graphs to AMR graphs'''
class UMR2AMR:
    split_roles = {
        ":material " : ":consist-of ", 
        ":part ": ":part ",
        ":concessive-condition ": ":condition ", 
        ":other-role " : ":mod ",
        ":group " : ":consist-of ", 
        ":start " : ":source ",
        ":goal " : ":destination ",
        ":recipient " : ":destination ",
        ":reason " : ":cause ",
        ":other-role " : ":mod "
    }
    
    new_roles_first = {
        ":causer " : ":ARG0 ", 
        ":force " : ":ARG0 ",
        ":actor " : ":ARG0 ",
        ":theme " : ":ARG1 ",
        ":undergoer " : ":ARG1 ",
        ":substitute " : ":instead-of-91"
    }

    new_roles_second = {
        ":experiencer" : [":ARG0", ":ARG1"], 
        ":stimulus" : [":ARG0", ":ARG1"], 
    }

    renamed_roles = {
        ":place" : ":location",
        ":temporal" : ":time",
        ":temporal-of" : ":time-of",
        ":companion" : ":accompanier",
        ":affectee" : ":beneficiary",
        ":list-item" : ":li",
        ":degree intensifier" : ":degree (v / very)",
        ":degree downtoner" : ":degree (s / somewhat)",
        ":degree equal" : ":degree (sa / same-01)"
    }

    modal_mappings = {
        ":modal-strength full-negative" : ":polarity -",
        ":modal-strength partial-negative" : ":polarity",
    }

    predication_mappings = {
        "individual-person" : "person",
        "belong-91" : "belong-01", 
        "have-91" : "have-03", 
        "have-rel-role-92" : "have-rel-role-91", 
        "have-org-role-92" : "have-org-role-91",
        "have-role-91" : ["have-rel-role-91", "have-org-role-91"], 
        "exist-91" : "be-located-at-91",
        "identity-91" : "same-01",
        "have-location-91" : "be-located-at-91"
    }

    ninetyone_roles = {
        "cite-91" : "cite-01",
        "infer-91" : "infer-01",
        "mean-91" : "mean-01",
        "resemble-91" : "resemble-01"
    }

    reification_roles = {
        # renamed roles
        "have-location-91" : "be-located-at-91",
        "have-temporal-91" : "be-temporally-at-91",
        "have-companion-91" : "accompany-01",
        "have-affectee-91" : "benefit-01",
        "have-list-item-91" : "have-li-91",
        # split roles
        "have-other-role-91" : "have-mod-91",
        "have-cause-91" : "cause-01",
        "have-reason-91" : "cause-01", 
        "have-group-91" : "consist-01",
        "have-material-91" : "consist-01", # active choice to convert have-material-91 to consist-01
        "have-source-91" : "be-from-91",
        "have-start-91" : "be-from-91",
        "have-goal-91" : "be-destined-for-91",
        "have-recipient-91" : "be-destined-for-91",
        "have-direction-91" : "be-destined-for-91",
        # unchanged roles
        "have-direction-91" : "be-destined-for-91",
        "have-path-91" : "be-destined-for-91",
        "have-duration-91" : "last-01",
        "have-91" : "have-03", # active choice to convert have-91 to have-03
        "have-topic-91" : "concern-02",
        "have-age-91" : "age-01",
        "have-example-91" : "exemplify-01"
    }

    pronoun_roles = {
        ":refer-person 2nd :refer-number singular" : "you",
        ":refer-person 2nd :refer-number plural" : "you",
        ":refer-person 2nd :refer-number dual" : "you",
        ":refer-person 1st :refer-number singular" : "i",
        ":refer-person 1st :refer-number plural" : "we",
        ":refer-person 1st :refer-number dual" : "we",
        ":refer-person 3rd :refer-number singular" : "they",
        ":refer-person 3rd :refer-number plural" : "they",
        ":refer-person 3rd :refer-number dual" : "they",
        # no consistency on order of :refer-person and :refer-number, so both orders are listed
        ":refer-number singular :refer-person 2nd" : "you",
        ":refer-number plural :refer-person 2nd" : "you",
        ":refer-number dual :refer-person 2nd" : "you",
        ":refer-number singular :refer-person 1st" : "i",
        ":refer-number plural :refer-person 1st" : "we",
        ":refer-number dual :refer-person 1st" : "we",
        ":refer-number singular :refer-person 3rd" : "they",
        ":refer-number plural :refer-person 3rd" : "they",
        ":refer-number dual :refer-person 3rd" : "they",
        ":refer-person 3rd" : "they",
        ":refer-person 2nd" : "you",
        ":refer-person 1st" : "i"
    }

    # This dictionary is adapted from umrlib by Jayeol Chun 
    # (https://github.com/umr4nlp/umrlib/blob/main/src/structure/amr2umr.py) Lines 70-74
    ''''''
    umr_roles = {
        'umr-unknown': 'amr-unknown',
        'umr-choice': 'amr-choice',
        'umr-empty': 'amr-empty',
        'umr-unintelligible': 'amr-unintelligible',
    }

    '''Removed instances of aspect and habitual as they do not appear in AMR, removed :modstr full affr as it is implied,
    and removed isolate instances of ref-num as it does not appear in AMR graphs'''
    removed_roles = {
        ":aspect habitual" : "",
        ":aspect imperfective" : "",
        ":aspect process" : "",
        ":aspect atelic-process" : "",
        ":aspect perfective" : "",
        ":aspect state" : "",
        ":aspect activity" : "",
        ":aspect endeavor" : "",
        ":aspect performance" : "",
        ":modal-strength full-affirmative" : "",
        ":mode interrogative" : "",
        ":mode imperative" : "",
        ":mode expressive" : "",
        ":refer-number singular" : "",
        ":refer-number plural" : ""
    }

    '''Finds the node in which a keyword is in'''
    def find_node(self, word, graph):
        word_ind = graph.find(word)
        if word_ind == -1:
            return None
        open_par_ind = graph.rfind("(", 0, word_ind)
        close_par_ind = graph.rfind(")", 0, word_ind)
        if close_par_ind > open_par_ind:
            balance = 0
            for i in range(close_par_ind, -1, -1):
                if graph[i] == "(":
                    balance -= 1
                elif graph[i] == ")":
                    balance += 1
                if balance == -2:
                    open_par_ind = i
                    break
        if open_par_ind == -1:
            return None
        balance = 1
        i = open_par_ind + 1
        while i < len(graph) and balance > 0:
            if graph[i] == "(":
                balance += 1
            elif graph[i] == ")":
                balance -= 1
            i += 1
        if balance == 0:
            return graph[open_par_ind:i].strip()
        else:
            return None

    '''Processes the UMR new roles and changes them to their AMR equivalents as set in dicts new_roles_first and new_roles_second'''
    def process_new_role(self, line):
        for umr_term, amr_term in self.new_roles_first.items():
            if umr_term in line:
                line = line.replace(umr_term, amr_term)
        for umr_term, amr_term in self.new_roles_second.items():
            '''Determines how :stimulus and :experiencer get mapped based on nodes set ARG values'''
            if umr_term in line:
                stim_node = self.find_node(":stimulus", line)
                exp_node = self.find_node(":experiencer", line)
                if umr_term == ":stimulus" and stim_node:
                    # if there is already in ARG0 in the node then set :stimulus to be ARG1, else set it to ARG0
                    if ":ARG0 " in stim_node: 
                        line = line.replace(umr_term, amr_term[1])
                    else:
                        line = line.replace(umr_term, amr_term[0])
                elif umr_term == ":experiencer" and exp_node:
                    # if there is already in ARG0 in the node then set :experiencer to be ARG1, else set it to ARG0
                    if ":ARG0 " in exp_node:
                        line = line.replace(umr_term, amr_term[1])
                    else:
                        line = line.replace(umr_term, amr_term[0])        
        return line

    '''Processes the UMR removed roles and changes them to their AMR equivalents as set in dict removed_roles'''
    def process_removed_role(self, line):
        for umr_term, amr_term in self.removed_roles.items():
            if umr_term in line:
                line = line.replace(umr_term, amr_term)
        return line

    '''Processes the UMR renamed roles and changes them to their AMR equivalents as set in dict renamed_roles'''
    def process_renamed_role(self, line):
        for umr_term, amr_term in self.renamed_roles.items():
            if umr_term in line:
                line = line.replace(umr_term, amr_term)
        return line

    '''Processes the UMR renamed roles and changes them to their AMR equivalents as set in dict split_roles'''
    def process_split_role(self, line):
        for umr_term, amr_term in self.split_roles.items():
            if umr_term in line:
                line = line.replace(umr_term, amr_term)
        return line

    '''Processes the UMR renamed roles and changes them to their AMR equivalents as set in dict umr_roles'''
    def process_umr_role(self, line):
        for umr_term, amr_term in self.umr_roles.items():
            if umr_term in line:
                line = line.replace(umr_term, amr_term)
        return line

    '''Processes the UMR renamed roles and changes them to their AMR equivalents as set in dict ninetyone_roles'''
    def process_ninetyone_role(self, line):
        for umr_term, amr_term in self.ninetyone_roles.items():
            if umr_term in line:
                line = line.replace(umr_term, amr_term)
        return line

    '''Processes the UMR renamed roles and changes them to their AMR equivalents as set in dict reification_roles'''
    def process_reification_role(self, line):
        for umr_term, amr_term in self.reification_roles.items():
            if umr_term in line:
                line = line.replace(umr_term, amr_term)
        return line

    '''Removes wikis from UMR graphs'''
    def process_wiki(self, line):
        wiki_pos = line.find(":wiki")
        if wiki_pos == -1:
            return line
        start_pos = wiki_pos + len(":wiki")
        if '(' in line[start_pos:]:
            open_paren_pos = line.find('(', start_pos)
            close_paren_pos = line.find(')', open_paren_pos)
            if open_paren_pos != -1 and close_paren_pos != -1:
                line = line[:wiki_pos] + line[close_paren_pos + 1:]
            else:
                line = line[:wiki_pos] + line[start_pos:].split(':', 1)[0].split(')', 1)[0]
        else:
            line = line[:wiki_pos] + line[start_pos:].split(':', 1)[0].split(')', 1)[0]

        return line

    '''Removes :quote and anthing following it'''
    def process_quote(self, line):
        line = re.sub(r":quote [^):]*(?=[):\(|$])", "", line)
        return line

    '''Removes the UMR role vocative and changes it so (s / say :ARG2 (whole graph))'''
    def process_vocative(self, line):
        if ":vocative (" in line:
            start_ind = line.find(":vocative (") + len(":vocative (")
            open_parens_count = 1
            end_ind = start_ind
            while open_parens_count > 0 and end_ind < len(line):
                if line[end_ind] == '(':
                    open_parens_count += 1
                elif line[end_ind] == ')':
                    open_parens_count -= 1
                end_ind += 1
            node_str = line[start_ind:end_ind - 1]
            node = self.find_node(node_str, line)
            final_str = f"(s / say :ARG2 {node})"
            line = line.replace(":vocative (" + node_str + ")", final_str)
            return line
        else:
            return line

    '''Processes the UMR renamed roles and changes them to their AMR equivalents as set in dict predication_mappings'''
    def process_predication(self, line):
        for umr_term, amr_term in self.predication_mappings.items():
            if umr_term in line:
                if umr_term == "have-role-91":
                    node = self.find_node("have-role-91", line)
                    if "organization" in node:
                        line = line.replace(umr_term, amr_term[1])
                    else:
                        line = line.replace(umr_term, amr_term[0])
                elif umr_term in ["belong-91", "have-91"]:
                    line = re.sub(r":ARG1", ":ARG0", line)
                    line = re.sub(r":ARG2", ":ARG1", line)
                elif umr_term == "exist-91":
                    line = re.sub(r":ARG1", r":ARG3", line)
                    line = re.sub(r":ARG2", r":ARG1", line)
                    line = re.sub(r":ARG3", r":ARG2", line)
                elif umr_term == "have-rel-role-92":
                    line = re.sub(r":ARG1", ":ARG0", line)
                    line = re.sub(r":ARG2", ":ARG1", line)
                    line = re.sub(r":ARG3", ":ARG2", line)
                    line = re.sub(r":ARG4", ":ARG3", line)
                else:
                    line = line.replace(umr_term, amr_term)
        return line

    '''Processes the UMR renamed roles and changes them to their AMR equivalents as set in dict modal_mappings'''
    def process_modality(self, line):
        for umr_term, amr_term in self.modal_mappings.items():
            if ":modal-strength partial-affirmative" in line:
                line = re.sub(r":modal-strength partial-affirmative", "", line)
                line = f"(r / recommend-01 :ARG1 {line.strip()})"
            elif ":modal-strength neutral-affirmative" in line:
                line = re.sub(r":modal-strength neutral-affirmative", "", line)
                line = f"(p / possible-01 :ARG1 {line.strip()})"
            else:
                line = line.replace(umr_term, amr_term)
        return line

    '''Processes the UMR renamed roles and changes them to their AMR equivalents as set in dict pronoun_roles'''
    def process_pronouns(self, line):
        for umr_term, amr_term in self.pronoun_roles.items():
            if umr_term in line:
                start_ind = line.find(umr_term)
                next_char = line[start_ind + len(umr_term)]
                if next_char == ")":
                    # if proceeded by "person " then replace node with amr_term
                    replace_str = umr_term
                    curr_ind = start_ind - 1
                    while len(replace_str) < (len(umr_term) + len("person ")):
                        replace_str = line[curr_ind] + replace_str
                        curr_ind -= 1
                    if replace_str == f"person {umr_term}":
                        line = line.replace(replace_str, amr_term)
                    # else, delete from line
                    else:
                        line = line.replace(umr_term, "")
                else: 
                    replace_str = umr_term
                    curr_ind = start_ind - 1
                    while line[curr_ind] != "/":
                        replace_str = line[curr_ind] + replace_str
                        curr_ind -= 1
                    line = line[:curr_ind] + "/ " + amr_term + line[start_ind + len(umr_term):]
        return line
 
    '''Method to check if the graph is balanced'''
    def count_parens(self, line):
        balanced = 0
        for char in line:
            if char == "(":
                balanced += 1
            if char == ")":
                balanced -= 1
        if balanced == 0:
            final_str = f"Balanced."
        else:
            final_str = f"Unbalanced..."
        return final_str
            
    '''Method to process all methods and conversion on a linearized graph'''
    def process_line(self, line):
        line = self.process_predication(line)
        line = self.process_modality(line)
        line = self.process_pronouns(line)
        line = self.process_split_role(line)
        line = self.process_umr_role(line)
        line = self.process_reification_role(line)
        line = self.process_ninetyone_role(line)
        line = self.process_wiki(line)
        line = self.process_quote(line)
        line = self.process_renamed_role(line)
        line = self.process_vocative(line)
        line = self.process_new_role(line)
        line = self.process_removed_role(line)
        return line

    '''Method to complete conversion'''
    def conversion(self, infile):
        outfile = infile.rsplit('.', 1)[0] + '_umr2amr.txt'
        with open(infile, 'r') as file:
            data = file.readlines()
        transformed_data = [self.process_line(line) for line in data]
        with open(outfile, 'w') as file:
            file.writelines(transformed_data)

