<template>
  <div id="map__container">
    <div id="map"/>
  </div>
</template>

<script>
  import mapboxgl from 'mapbox-gl/dist/mapbox-gl';
  import MapboxLanguage from '@mapbox/mapbox-gl-language';
  import gjs from './geojson.service';
  import ds  from './data.service';

  export default {
    data: () => ({
      map: null
    }),
    mounted() {
      mapboxgl.accessToken = 'pk.eyJ1IjoieXVuZ3ZsZGFpIiwiYSI6ImNqeThkbWg2OTAzYnEzZHBud2wyZW9tYmsifQ.XpqSXSU5y7PW60b0TAQb9w';
      this.map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v10',
        zoom: 10,
        center: [30.315868, 59.939095]
      });
      this.map.on('load', this.onMapLoad);
      ds.getData();
    },
    methods: {
      onMapLoad() {
        this.map.addControl(new mapboxgl.NavigationControl({ showCompass: false }));
        this.drawDistricts();
      },
      drawDistricts() {
        /*
         * districts structure
         * {
         *   relation: <district_openstreetmap_relation>,
         *   desc: <description> ,
         *   color: <color>
         * }
        */
        const districts = [
          { relation: 1114354, color: '#C0392B', desc: 'Выборгский район', uik: [199, 401]},
          { relation: 368287, color: '#9B59B6', desc: 'Невский район' },
          { relation: 1114806, color: '#2980B9', desc: 'Калининский район', uik: [414, 548] },
          { relation: 1115367, color: '#1ABC9C', desc: 'Приморский район' },
          { relation: 1114193, color: '#F1C40F', desc: 'Адмиралтейский район', uik: [1, 61]},
          { relation: 1114895, color: '#D35400', desc: 'Красногвардейский район', uik: [901, 1047]},
          { relation: 1115366, color: '#2BE211', desc: 'Курортный район'},
          { relation: 1114905, color: '#11E2D1', desc: 'Петроградский район'},
          { relation: 338635, color: '#DA11E2', desc: 'Пушкинский район'},
          { relation: 1114252, color: '#F59797', desc: 'Василеостровский район', uik: [104, 179]},
          { relation: 1114809, color: '#869510', desc: 'Кировский район', uik: [576, 814]},
          { relation: 363103, color: '#101200', desc: 'Красносельский район', uik: [1145]},
          { relation: 338636, color: '#196B1D', desc: 'Московский район'},
          { relation: 1114902, color: '#19296B', desc: 'Центральный район'},
          { relation: 367375, color: '#6B1919', desc: 'Петродворцовый район'},
          { relation: 369514, color: '#00FF00', desc: 'Фрунзенский район'},
          { relation: 337424, color: '#003AFF', desc: 'Колпинский район', uik: [826, 892]},
          { relation: 1115082, color: '#FF0000', desc: 'Кронштадтский район'}
        ];
        this.loadPolygons(districts, polygon => {
          this.map.addSource(polygon.id, polygon.source);
          this.map.addLayer(
            gjs.compileLayer(polygon.id, polygon.color, 0.7)
          );
        });
      },
      loadPolygons(districts, drawCallback) {
        districts.forEach(district => {
          gjs.getRelation(district.relation)
          .then(response => {
            drawCallback({
              id: `district${district.relation}`,
              color: district.color,
              source: {
                type: 'geojson',
                data: gjs.convert(response.data)
              },
              desc: district.desc
            });
          })
          .catch(error => {
            console.log(error);
          });
        });
      }
    }
  }
</script>

<style>
  #map__container {
    position: fixed;
    top: 0px;
    left: 0px;
    width: 100%;
    height: 100%;
  }

  #map {
    width: 100%;
    height: 100%;
  }
</style>
