from git import Repo
import shutil


class RepositoryManager:
    """
    This class exists to clone and cleanup repositories in an isolated
    manner so that git operations are separate from business logic.
    """

    def __init__(self):
        self.cloned_repositories = []

    def clone_repository(self, repository):
        """
        Clone the repository into a local directory with the name of the .ini section
        :param repository to be processed
        """
        repo = Repo.clone_from(repository.git_url, repository.name)
        self.cloned_repositories.append((repo, repository.name))

    def remove_repositories(self):
        """
        Close the git session and remove the created directories
        :return: None
        """
        for repository, repo_dir in self.cloned_repositories:
            repository.close()
            shutil.rmtree(repo_dir)


class RepositoryConfiguration:
    """
    Internal representation of all the relevant information for a given repository
    """

    def __init__(self, name: str, git_url: str, files: list, binding_urls: list):
        self.name = name
        self.git_url = git_url
        self.files = files
        self.binding_urls = binding_urls

    def __str__(self):
        return f'{self.name} @ {self.git_url}'

