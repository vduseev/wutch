const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))

async function wutch() {
  while (true) {
    fetch("http://localhost:50231")
      .then((response) => {
        if (response.status == 200) {
          return response.json()
        }
      })
      .then(response => {
        if (response.status == "changed") {
          window.location.reload();
        }
      })
      .catch((error) => {});

    await sleep(1000);
  }
}
