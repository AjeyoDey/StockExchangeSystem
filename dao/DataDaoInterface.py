# Data objects Simulating an in-memory data-store, mocking a DB
import abc


class DataDaoInterface(abc.ABC):
    @abc.abstractmethod
    def addData(self, data):
        raise Exception("Not Implemented")

    @abc.abstractmethod
    def updateDataStatus(self, data_id: str):
        raise Exception("Not Implemented")

    @abc.abstractmethod
    def getDataById(self, data_id):
        raise Exception("Not Implemented")

    @abc.abstractmethod
    def getDataByFilter(self):
        # Supposed to use filters to fetch Data from Store
        raise Exception("Not Implemented")