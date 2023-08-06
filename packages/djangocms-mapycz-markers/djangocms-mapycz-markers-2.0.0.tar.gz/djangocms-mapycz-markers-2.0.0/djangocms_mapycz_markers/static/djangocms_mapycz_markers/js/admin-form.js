function addressSuggest() {
    const address = document.getElementById("id_address")
    const longitude = document.getElementById("id_longitude")
    const latitude = document.getElementById("id_latitude")
    const title = document.getElementById("id_title")
    const card_body = document.getElementById("id_card_body")
    const suggest = new SMap.Suggest(address)
    // Restriction for the Czechia.
    suggest.urlParams({bounds: "48.5370786,12.0921668|51.0746358,18.8927040"})
    suggest.addListener("suggest", function(suggestData) {
      address.value = suggestData.prevPhrase
      if (suggestData.data.longitude && suggestData.data.latitude) {
        longitude.value = suggestData.data.longitude
        latitude.value = suggestData.data.latitude
        title.value = suggestData.data.title
        card_body.value = suggestData.data.title + "\n" + suggestData.data.secondRow
        if (suggestData.data.thirdRow) {
          card_body.value += "\n" + suggestData.data.thirdRow
        }
      }
    })
}

function initAddressSuggest() {
    Loader.load(null, {suggest: true}, addressSuggest)
}

window.addEventListener("load", initAddressSuggest)
