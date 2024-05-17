from requests import Session
from uuid import uuid4
from utils.time_utils import measureTime, measureTimeString
from concurrent.futures import ThreadPoolExecutor, as_completed


class APIHandler:
    def __init__(self):
        self._url = "https://www.adozionilibriscolastici.it"
        self._session_id = None
        self._session = None

    def get_session(self):
        if self._session is None:
            self._session = self.create_session()
        return self._session

    def get_session_id(self):
        if self._session_id is None:
            self.create_session_id()
        return self._session_id

    def create_session_id(self):
        self._session_id = uuid4()

    def create_session(self):
        print(f"Creating a new session with ID: {self.get_session_id()}")
        session = Session()
        session.get(self._url)
        return session

    def get_data(self, url):
        data = None
        session = self.get_session()
        response = session.get(url)

        if response.status_code == 200:
            data = response.json()
        else:
            print(f"APIHandler ({self.get_session_id()}): Errore {response.status_code} -> {url}!")
        return data

    def get_libri_adottati(self, classe_id, scuola_id="VRTF03000V"):
        api_url = f"https://www.adozionilibriscolastici.it/v1/libri"
        url = f"{api_url}/{classe_id}/{scuola_id}"
        return self.get_data(url)

    def close_session(self):
        if self._session:
            self._session.close()
        # self._session.cookies.clear()
        # self._session.headers.clear()
        # self._session.params = {}
        # self._session.auth = None
        self._session.headers.update({'Connection': 'close'})
        self._session.get(self._url)
        del self._session
        self._session = None


def fetch_books_parallel(api_handler, classe_ids):
    results = []
    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = [executor.submit(api_handler.get_libri_adottati, classe_id) for classe_id in classe_ids]
        for future in as_completed(futures):
            results.append(future.result())
    return results


def process_block(blocco_classe_ids):
    api_handler = APIHandler()
    print(blocco_classe_ids)
    api_handler.get_session()
    results = fetch_books_parallel(api_handler, blocco_classe_ids)
    print(results)
    api_handler.close_session()
    del api_handler


def main():
    tupleTime = measureTime()

    classe_ids = [558988, 558989, 558990, 558991, 558992, 558993, 558994, 558995, 558996, 558997, 558998, 558999,
                  559000, 559001, 559002, 559003, 559004, 559005, 559006, 559007, 559008, 559009, 559010, 559011,
                  559013, 559014, 559015, 559016, 559017, 559018, 559021, 559022, 559023, 559024, 559025, 559026,
                  559027, 559028, 559029, 559030, 559031, 559032, 559033, 559034, 559035, 559037, 559038, 559039,
                  559040, 559041, 559042, 559043, 559044, 559045, 559046, 559048, 559049, 559050, 559051, 988355,
                  988357, 988359, 988360, 1102808, 1102809, 1102810, 1102811, 1102812, 1102813, 1102814, 1102815]

    num_threads = 15
    blocchi_classe_ids = [classe_ids[i:i + num_threads] for i in range(0, len(classe_ids), num_threads)]

    for blocco_classe_ids in blocchi_classe_ids:
        process_block(blocco_classe_ids)
    print(f"time: {measureTimeString(tupleTime)}")


if __name__ == "__main__":
    main()
