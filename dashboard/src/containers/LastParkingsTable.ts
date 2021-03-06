import * as moment from 'moment';
import { connect } from 'react-redux';
import ReactTable, { TableProps } from 'react-table';

import 'react-table/react-table.css';

import { Parking, ParkingProperties, RootState } from '../types';

let langFile = require('../languages/en-EN.json');
var language = window.navigator.language;
try {
  langFile = require('../languages/'.concat(language, '.json'));
} catch {
  langFile = require('../languages/en-EN.json');
}
let stringData = JSON.stringify(langFile);
let lang = JSON.parse(stringData);

interface ParkingData extends ParkingProperties {
    id: string;
}

function getDataOfParking(parking?: Parking): ParkingData|undefined {
    return (parking) ? {
        id: parking.id,
        ...parking.properties,
    } : undefined;
}

function formatTime(timestamp?: number|null): string|undefined {
    if (!timestamp) {
        return undefined;
    }
    return moment(timestamp).format('L LTS');
}

function mapStateToProps(state: RootState): Partial<TableProps> {
    const {dataTime, parkings, selectedRegion, validParkingsHistory} = state;
    const validParkings = validParkingsHistory[dataTime || 0] || [];

    const data = validParkings.map(
        (parkingId: string) => getDataOfParking(parkings[parkingId])).filter(
            (d?: ParkingData) =>
                (d && (!selectedRegion || d.region === selectedRegion)));

    const columns = [
        {
            Header: lang.id,
            accessor: 'id',
        }, {
            Header: lang.registrationNumber,
            accessor: 'registrationNumber',
        }, {
            Header: lang.operatorName,
            accessor: 'operatorName',
        }, {
            Header: lang.zone,
            accessor: 'zone',
        }, {
            Header: lang.terminalNumber,
            accessor: 'terminalNumber',
        }, {
            Header: lang.timeStart,
            id: 'timeStart',
            accessor: (d: ParkingData) => formatTime(d.timeStart),
        }, {
            Header: lang.timeEnd,
            id: 'timeEnd',
            accessor: (d: ParkingData) => formatTime(d.timeEnd),
        }, {
            Header: lang.createdAt,
            id: 'createdAt',
            accessor: (d: ParkingData) => formatTime(d.createdAt),
        }, {
            Header: lang.modifiedAt,
            id: 'modifiedAt',
            accessor: (d: ParkingData) => formatTime(d.modifiedAt),
        },
    ];

    return {data, columns};
}

const mapDispatchToProps = null;

const LastParkingsTable = connect(
    mapStateToProps, mapDispatchToProps)(ReactTable);

export default LastParkingsTable;
