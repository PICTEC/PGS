declare module 'react-leaflet-markercluster' {
  import { Component } from 'react';
  
  export interface MarkerClusterGroupProps {
    maxClusterRadius: (zoom: number) => number;
  }
  export default class MarkerClusterGroup extends Component<MarkerClusterGroupProps> {}
}
