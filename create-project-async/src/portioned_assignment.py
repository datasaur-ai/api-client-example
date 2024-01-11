import glob
from enum import Enum
from itertools import combinations
from src.exceptions.invalid_options import InvalidOptions

class AssignmentRole(Enum):
  LABELER = "LABELER"
  REVIEWER = "REVIEWER"
  HYBRID = "LABELER_AND_REVIEWER"

class PortionedAssignment:
    def __init__(self, old_assignments: list[dict], multi_pass_prefix: str, single_pass_prefix: str, multi_pass_labeler_count: int):
        self.original_assignments = old_assignments if old_assignments else []
        self.multi_pass_prefix = multi_pass_prefix
        self.single_pass_prefix = single_pass_prefix
        self.multi_pass_labeler_count = multi_pass_labeler_count

        # maps teamMemberId to original assignment role
        self.original_role_map: dict[str, str] = {}
        for assignment in self.original_assignments:
            team_member_id = assignment["teamMemberId"];
            role = assignment["role"]
            self.original_role_map[team_member_id] = role


    def create_new_assignments_by_documents(self, documents_path):
        if (len(self.original_assignments) == 0):
            return self.original_assignments

        # splits single-pass and multi-pass files
        multi_pass_file_names = []
        single_pass_file_names = []
        for filepath in glob.iglob(f"{documents_path}/*"):
            file_name = filepath.split('/')[-1]
            if file_name.startswith(self.multi_pass_prefix):
                multi_pass_file_names.append(file_name);

            if file_name.startswith(self.single_pass_prefix):
                single_pass_file_names.append(file_name);


        if (len(multi_pass_file_names) == 0 and len(single_pass_file_names) == 0):
            raise InvalidOptions(f'No valid multi-pass and single-pass files found. Please check the contents inside {documents_path} and make sure the file names have the correct prefixes')

        return self.distribute_assignments(multi_pass_file_names=multi_pass_file_names, single_pass_file_names=single_pass_file_names)

    def distribute_assignments(self, multi_pass_file_names: list[str], single_pass_file_names: list[str]):
        # split reviewer and labeler assignees
        # labeler assignees include `LABELER_AND_REVIEWER` role
        labeler_team_member_ids = []
        reviewer_team_member_ids = []
        for assignment in self.original_assignments:
            team_member_id = assignment["teamMemberId"]
            role = assignment["role"]

            if (role == AssignmentRole.REVIEWER):
                reviewer_team_member_ids.append(team_member_id)
            else:
                labeler_team_member_ids.append(team_member_id)

        labeler_assignments = self.distribute_labeler_assignments(
            team_member_ids=labeler_team_member_ids,
            multi_pass_file_names=multi_pass_file_names,
            single_pass_file_names=single_pass_file_names)

        reviewer_assignments = self.distribute_reviewer_assignments(
            team_member_ids=reviewer_team_member_ids,
            multi_pass_file_names=multi_pass_file_names,
            single_pass_file_names=single_pass_file_names)

        return labeler_assignments + reviewer_assignments


    def distribute_labeler_assignments(self, team_member_ids: list[str], multi_pass_file_names: list[str], single_pass_file_names: list[str]):
        # maps teamMemberId to list of file names (initially empty)
        assignment_map: dict[str, list[str]] = {str(id): [] for id in team_member_ids}

        # assign single pass labelers
        for i, file_name in enumerate(single_pass_file_names):
            team_member_id = team_member_ids[i % len(team_member_ids)]
            assignment_map[team_member_id].append(file_name)

        # assign multi pass labelers
        team_member_id_combinations = list(combinations(team_member_ids, self.multi_pass_labeler_count))
        num_combinations = len(team_member_id_combinations)
        for i, file_name in enumerate(multi_pass_file_names):
            combination = team_member_id_combinations[i % num_combinations]
            for team_member_id in combination:
                assignment_map[team_member_id].append(file_name)

        # convert assignment_map to list of assignments
        assignments: list[dict] = []
        for team_member_id in assignment_map.keys():
            file_names = assignment_map.get(team_member_id)
            role = self.original_role_map.get(team_member_id)
            if file_names:
                assignments.append(self.create_assignment(team_member_id=team_member_id, file_names=file_names, role=role))

        return assignments


    def distribute_reviewer_assignments(self, team_member_ids: list[str], multi_pass_file_names: list[str], single_pass_file_names: list[str]):
        assignments: list[dict] = []
        file_names = multi_pass_file_names + single_pass_file_names
        # REVIEWER role assignees get all the documents
        for team_member_id in team_member_ids:
            assignments.append(self.create_assignment(team_member_id=team_member_id, file_names=file_names, role="REVIEWER"))

        return assignments


    def create_assignment(self, team_member_id: str, file_names: list[str], role: str | None):
        documents = []
        for file_name in file_names:
            documents.append({
                "fileName": file_name,
                "part": 0
            })

        return {
            "teamMemberId": team_member_id,
            "documents": documents,
            "role": role,
        }

    @staticmethod
    def validate(operations):
        split_files_config = operations["variables"]["input"]["creationSettings"]["splitDocumentConfig"]
        if split_files_config is not None:
            raise InvalidOptions("Portioned assignments does not support documents splitting.")
