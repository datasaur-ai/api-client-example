import glob
from itertools import combinations
import json
from src.exceptions.invalid_options import InvalidOptions

class PortionedAssignment:
    def __init__(self, old_assignments: list[dict], multi_pass_prefix: str, single_pass_prefix: str, multi_pass_labeler_count: int):
        self.old_assignments = old_assignments if old_assignments else []
        self.multi_pass_prefix = multi_pass_prefix
        self.single_pass_prefix = single_pass_prefix
        self.multi_pass_labeler_count = multi_pass_labeler_count


    def create_new_assignments_by_documents(self, documents_path):
        if (len(self.old_assignments) == 0):
            return self.old_assignments


        multi_pass_documents = []
        single_pass_documents = []

        for filepath in glob.iglob(f"{documents_path}/*"):
            filename = filepath.split('/')[-1]
            if filename.startswith(self.multi_pass_prefix):
                multi_pass_documents.append(filename);

            if filename.startswith(self.single_pass_prefix):
                single_pass_documents.append(filename);


        if (len(multi_pass_documents) == 0 and len(single_pass_documents) == 0):
            raise InvalidOptions(f'No valid multi-pass and single-pass files found. Please check the contents inside {documents_path} and make sure the file names have the correct prefixes')

        return self.distribute_assignments(multi_pass_documents=multi_pass_documents, single_pass_documents=single_pass_documents)

    def distribute_assignments(self, multi_pass_documents: list[str], single_pass_documents: list[str]):
        if (self.old_assignments == None):
            return self.old_assignments

        labeler_team_member_ids = []
        reviewer_team_member_ids = []

        for assignment in self.old_assignments:
            team_member_id = assignment["teamMemberId"]
            role = assignment["role"]

            if (role == "REVIEWER"):
                reviewer_team_member_ids.append(team_member_id)
            else:
                labeler_team_member_ids.append(team_member_id)

        labeler_assignments = self.distribute_labeler_assignments(
            team_member_ids=labeler_team_member_ids,
            multi_pass_documents=multi_pass_documents,
            single_pass_documents=single_pass_documents)

        reviewer_assignments = self.distribute_reviewer_assignments(
            team_member_ids=reviewer_team_member_ids,
            multi_pass_documents=multi_pass_documents,
            single_pass_documents=single_pass_documents)

        return labeler_assignments + reviewer_assignments


    def distribute_labeler_assignments(self, team_member_ids: list[str], multi_pass_documents: list[str], single_pass_documents: list[str]):
        if len(team_member_ids) < self.multi_pass_labeler_count:
            raise InvalidOptions('multi_pass_labeler_count value must not exceed the number of assignments with LABELER role.')

        # maps teamMemberId to list of file names (initially empty)
        assignment_map: dict[str, list[str]] = {str(id): [] for id in team_member_ids}

        # assign single pass labelers
        for i, file_name in enumerate(single_pass_documents):
            team_member_id = team_member_ids[i % len(team_member_ids)]
            assignment_map[team_member_id].append(file_name)

        # assign multi pass labelers
        team_member_id_combinations = list(combinations(team_member_ids, self.multi_pass_labeler_count))
        num_combinations = len(team_member_id_combinations)
        for i, file_name in enumerate(multi_pass_documents):
            combination = team_member_id_combinations[i % num_combinations]
            for team_member_id in combination:
                assignment_map[team_member_id].append(file_name)

        # convert assignment_map to list of assignments
        assignments: list[dict] = []
        for team_member_id in assignment_map.keys():
            file_names = assignment_map.get(team_member_id)
            if file_names:
                assignments.append(self.create_assignment(team_member_id=team_member_id, file_names=file_names))

        return assignments


    def distribute_reviewer_assignments(self, team_member_ids: list[str], multi_pass_documents: list[str], single_pass_documents: list[str]):
        assignments: list[dict] = []
        documents = multi_pass_documents + single_pass_documents
        for team_member_id in team_member_ids:
            assignments.append(self.create_assignment(team_member_id, documents))

        return assignments


    def create_assignment(self, team_member_id: str, file_names: list[str]):
        documents = []
        for file_name in file_names:
            documents.append({
                "fileName": file_name,
                "part": 0
            })

        return {
            "teamMemberId": team_member_id,
            "documents": documents
        }

    @staticmethod
    def validate(operations):
        split_files_config = operations["variables"]["input"]["creationSettings"]["splitDocumentConfig"]
        if split_files_config is not None:
            raise InvalidOptions("Portioned assignments does not support documents splitting.")