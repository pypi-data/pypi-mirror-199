import json
import os
import requests
import webbrowser


class DataStory:

    def __init__(self, name: str):
        self._name = name
        self._views = []

    def header(self, content: str, level: int = 2) -> None:
        """
        Add header to datastory.

        Parameters
        ----------
        content : str
            Header text
        level : int
            Size of header (default 2)

        Returns
        -------
        None
        """
        self._views.append({
            "type": "header",
            "spec": {
                "content": content,
                "level": level
            }
        })

    def markdown(self, md: str):
        """
        Add markdown to datastory.

        Parameters
        ----------
        md : str
            Markdown text

        Returns
        -------
        None
        """
        self._views.append({
            "type": "markdown",
            "spec": {
                "content": md
            }
        })

    def plotly(self, fig: str):
        """
        Add plotly graph to datastory.

        Expects figure data as JSON string.

        Parameters
        ----------
        fig : str
            Figure data as JSON string

        Returns
        -------
        None
        """
        self._views.append({
            "type": "plotly",
            "spec": json.loads(fig)
        })

    def vega(self, fig: str):
        """
        Add vega graph to datastory.

        Expects figure data as JSON string.

        Parameters
        ----------
        fig : str
            Figure data as JSON string

        Returns
        -------
        None
        """
        self._views.append({
            "type": "vega",
            "spec": json.loads(fig)
        })

    def _to_dict(self) -> dict:
        return {
            "name": self._name,
            "views": [view for view in self._views]
        }

    def publish(self, url: str = None) -> str:
        """
        Publish the datastory.

        Creates a new datastory draft.

        Parameters
        ----------
        url : str
            URL for datastory API

        Returns
        -------
        str
            URL to datastory draft.
        """
        if not url:
            url = os.getenv("DATASTORY_URL", "http://localhost:8080/api")

        res = requests.post(url+"/story", json=self._to_dict())
        res.raise_for_status()

        try:
            url = res.json()["url"]
        except KeyError as e:
            return f"invalid api response {e.__str__}"

        if not webbrowser.open(url):
            print(f"Gå til {url} for å se på draften din")

        return url

    def update(self, token: str, url: str = None) -> str:
        """
        Update the datastory.

        Updates a published datastory

        Parameters
        ----------
        token : str
            Datastory token used for updating existing datastory
        url : str
            URL for datastory API

        Returns
        -------
        str
            URL to published datastory.
        """
        if not url:
            url = os.getenv("DATASTORY_URL", "http://localhost:8080/api")

        res = requests.put(f"{url}/story", json=self._to_dict(),
                           headers={"Authorization": f"Bearer {token}"})
        res.raise_for_status()

        try:
            url = res.json()["url"]
        except KeyError as e:
            return f"invalid api response {e.__str__}"

        return url
