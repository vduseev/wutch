const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))

async function wutch() {
  while (true) {
    fetch("http://localhost:50231")
      .then(response => response.json())
      .then(response => {
        if (response.status == "changed") {
          window.location.reload();
        }
      });
    await sleep(1000);
  }
}
