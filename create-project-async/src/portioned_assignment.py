import glob
from itertools import combinations

# TODO: throw error if split files is enalbed in the operation
class PortionedAssignment:
    def __init__(self, old_assignments: list[dict] | None, multi_pass_prefix: str, single_pass_prefix: str, multi_pass_labeler_count: int):
        self.old_assignments = old_assignments
        self.multi_pass_prefix = multi_pass_prefix
        self.single_pass_prefix = single_pass_prefix
        self.multi_pass_labeler_count = multi_pass_labeler_count


    def adjust_assignments_by_documents(self, documents_path):
        if (self.old_assignments == None):
            return self.old_assignments

        multi_pass_documents = []
        single_pass_documents = []

        for filepath in glob.iglob(f"{documents_path}/*"):
            filename = filepath.split('/')[-1]
            if filename.startswith(self.multi_pass_prefix):
                multi_pass_documents.append(filename);

            if filename.startswith(self.single_pass_prefix):
                single_pass_documents.append(filename);

            print(filename)

        if (len(multi_pass_documents) == 0 and len(single_pass_documents) == 0):
            return self.old_assignments

        return self.portion_assignments(multi_pass_documents=multi_pass_documents, single_pass_documents=single_pass_documents)

    def portion_assignments(self, multi_pass_documents: list[str], single_pass_documents: list[str]):
        if (self.old_assignments == None):
            return self.old_assignments

        labeler_team_member_ids = []
        reviewer_team_member_ids = []

        for assignment in self.old_assignments:
            team_member_id = assignment["teamMemberId"]
            role = assignment["role"]

            if (role == "LABELER"):
                labeler_team_member_ids.append(team_member_id)

            if (role == "REVIEWER"):
                reviewer_team_member_ids.append(team_member_id)

        labeler_assignment_map: dict[str, list[str]] = {str(id): [] for id in labeler_team_member_ids}

        # assign single pass labelers
        for i, file_name in enumerate(single_pass_documents):
            team_member_id = labeler_team_member_ids[i % len(labeler_team_member_ids)]
            labeler_assignment_map[team_member_id].append(file_name)

        # assign multi pass labelers
        team_member_id_combinations = list(combinations(labeler_team_member_ids, self.multi_pass_labeler_count))
        num_combinations = len(team_member_id_combinations)

        for i, file_name in enumerate(multi_pass_documents):
            combination = team_member_id_combinations[i % num_combinations]
            for team_member_id in combination:
                labeler_assignment_map[team_member_id].append(file_name)

        assignments: list[dict] = []
        for team_member_id in labeler_assignment_map.keys():
            file_names = labeler_assignment_map.get(team_member_id)
            if file_names:
                assignments.append(self.create_assignment(team_member_id=team_member_id, file_names=file_names))




    def create_assignment(self, team_member_id: str, file_names: list[str]):
        documents = map(lambda file_name: {
            "fileName": file_name,
            "part": 0
        }, file_names)

        return {
            "teamMemberId": team_member_id,
            "documents": documents
        }