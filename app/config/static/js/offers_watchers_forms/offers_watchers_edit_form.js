const app = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {
            user_watchers_by_cities: Vue.reactive(JSON.parse(document.getElementById('user_watchers_by_cities').textContent)),
            selectedWatchersIds: new Set(),
            clickToDeleteWatherId: null,
            clickToDeleteWatherIdDisplayStyle: null,
        }
    },
    methods: {
        choiceSingleWatcherToDelete(watcherId){
            this.clickToDeleteWatherId = watcherId;
            this.clickToDeleteWatherIdDisplayStyle = watcherId;
            setTimeout(
             () => this.clickToDeleteWatherIdDisplayStyle = null,
             1500
            );
        },
        watcherChoicedToDelete(watcherId) {
            const intWatcherId = Number(watcherId);
            return this.selectedWatchersIds.has(intWatcherId) || this.clickToDeleteWatherIdDisplayStyle == intWatcherId
        },
        selectAll(city) {
            mainSelectCheckBox = document.getElementById('main-select-checkbox'.concat('-', city));
            if (mainSelectCheckBox.checked){
                needChecked = true;
            }
            else needChecked = false;

            checkboxes = document.getElementsByName('select-checkbox'.concat('-', city));
            for(var i=0, n=checkboxes.length;i<n;i++) {
                checkboxes[i].checked = needChecked;
            }

            if (needChecked){
                checkboxes.forEach(
                        checkbox => {
                            wactherId = Number(checkbox.value);
                            if (wactherId) this.selectedWatchersIds.add(wactherId);
                        }
                    );
            }
            else {
                checkboxes.forEach(
                        checkbox => {
                            wactherId = Number(checkbox.value);
                            if (wactherId) this.selectedWatchersIds.delete(wactherId);
                        }
                    );
            }

            console.log(this.selectedWatchersIds);
        },
        selectCheckbox: function(watcherOffersId) {
            eventCheckbox = document.getElementById('checkbox'.concat('-', watcherOffersId));
            if (eventCheckbox.checked) {
                this.selectedWatchersIds.add(Number(watcherOffersId));
            }
            else {
                this.selectedWatchersIds.delete(Number(watcherOffersId));
            }
            console.log(this.selectedWatchersIds);
        },
        deleteSingleOfferWatcher() {
                axios.delete("" ,{data: {"watchersIdsToDelete": [this.clickToDeleteWatherId]}})
                .then(function (response) {
                    this.user_watchers_by_cities = Vue.reactive(response.data.user_watchers_by_cities);
                    console.log(this.user_watchers_by_cities);
                })
                .catch(function (error) {
                    // handle error
                });
        }
    }
});

app.mount('#app');
console.log(JSON.parse(document.getElementById('user_watchers_by_cities').textContent));