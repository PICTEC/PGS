import { Point } from './components/types';

declare global {
  interface Window {
    _env_: {
      REACT_APP_API_CENTER: string;
      REACT_APP_API_URL: string;
    };
  }
}

export const isDev = false;

export const apiBaseUrl: string = window._env_.REACT_APP_API_URL;

let mapPoint: Point;

if (typeof window._env_.REACT_APP_API_CENTER !== 'undefined') {
    const envPoint = window._env_.REACT_APP_API_CENTER!.split(',').map(Number);
    mapPoint = [envPoint[0], envPoint[1]];
} else {
    mapPoint = [60.17, 24.94]; // Default to Helsinki centrum
}
export const centerCoordinates: Point = mapPoint;
