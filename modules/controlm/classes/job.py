class Job:
    def __init__(self, name, status="Pending", start_date=None, end_date=None):
        """
        Constructor for the Job class.

        :param name: str - Name of the job.
        :param status: str - Status of the job (e.g., Pending, Running, Completed, Failed).
        :param start_date: datetime or None - Start date of the job.
        :param end_date: datetime or None - End date of the job.
        """
        self.name = name
        self.status = status
        self.start_date = start_date
        self.end_date = end_date

    def set_status(self, status):
        """
        Update the status of the job.

        :param status: str - New status of the job.
        """
        self.status = status

    def set_start_date(self, start_date):
        """
        Set the start date of the job.

        :param start_date: datetime - Start date of the job.
        """
        self.start_date = start_date

    def set_end_date(self, end_date):
        """
        Set the end date of the job.

        :param end_date: datetime - End date of the job.
        """
        self.end_date = end_date

    def __str__(self):
        """
        String representation of the job.

        :return: str - Information about the job.
        """
        return (f"Job(Name: {self.name}, Status: {self.status}, "
                f"Start Date: {self.start_date}, End Date: {self.end_date})")

# Example usage
if __name__ == "__main__":
    from datetime import datetime

    # Create a new job
    job = Job(name="Data Extraction")

    # Set start date
    job.set_start_date(datetime.now())

    # Update status to Running
    job.set_status("Running")

    # Set end date and mark as Completed
    job.set_end_date(datetime.now())
    job.set_status("Completed")

    # Print job details
    print(job)
