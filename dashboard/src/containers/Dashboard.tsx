import { Dispatch } from 'redux';
import * as React from 'react';
import { connect } from 'react-redux';

import { Bar } from 'react-chartjs-2';
import { Button, Card, CardBody, CardGroup, CardHeader, Col, Container, Row } from 'reactstrap';

import * as dispatchers from '../dispatchers';
import { RootState, Timestamp } from '../types';
import LastParkingsTable from './LastParkingsTable';
import ParkingRegionsMap from './ParkingRegionsMap';
import TimeSelect from './TimeSelect';
import RegionSelector from './RegionSelector';
import fileDownload from 'js-file-download';
import * as moment from 'moment';

import './Dashboard.css';
import api from '../api';
import * as axios from 'axios';

var logo = require('./../assets/pgs_logo.png');

let langFile = require('../languages/en-EN.json');
var language = window.navigator.language;
try {
    langFile = require('../languages/'.concat(language, '.json'));
} catch {
    langFile = require('../languages/en-EN.json');
}
let stringData = JSON.stringify(langFile);
let lang = JSON.parse(stringData);

const bar = {
    labels: ['16', '18', '20', '22', '0', '2', '4', '6', '8', '10', '12', '14'],
    datasets: [
        {
            backgroundColor: 'rgba(255,99,132,0.2)',
            borderColor: 'rgba(255,99,132,1)',
            borderWidth: 1,
            hoverBackgroundColor: 'rgba(255,99,132,0.4)',
            hoverBorderColor: 'rgba(255,99,132,1)',
            data: [108, 95, 75, 35, 25, 21, 28, 35, 89, 81, 92, 99]
        }
    ]
};

interface Props {
    autoUpdate: boolean;
    onUpdate: () => void;
    onLogout: (event: React.MouseEvent<{}>) => void;
    dateTime: Timestamp|null;
}

type TimerId = number;

class Dashboard extends React.Component<Props> {
    timer: TimerId|null = null;
    timerInterval: number = 1000; // 1 second

    componentDidMount() {
        if (this.props.autoUpdate && !this.timer) {
            this.enableAutoUpdate();
        }
    }

    componentWillReceiveProps(nextProps: Props) {
        if (nextProps.autoUpdate && !this.timer) {
            this.enableAutoUpdate();
        }
        if (!nextProps.autoUpdate && this.timer) {
            this.disableAutoUpdate();
        }
    }

    enableAutoUpdate() {
        this.autoUpdate();
        if (this.timer) {
            return;  // Was already enabled
        }
        this.timer = window.setInterval(
            this.autoUpdate.bind(this), this.timerInterval);
    }

    disableAutoUpdate() {
        if (!this.timer) {
            return;  // Was already disabled
        }
        window.clearInterval(this.timer);
        this.timer = null;
    }

    autoUpdate() {
        if (this.props.onUpdate) {
            this.props.onUpdate();
        }
    }

    handleStatisticsDownload() {
        api.fetchStatistics(
            (response: axios.AxiosResponse) => fileDownload(response.data, 'statistics.csv'),
            (error: Error) => console.error('Cannot fetch statistics: ' + error),
            this.props.dateTime != null ? moment(this.props.dateTime) : undefined
        );
    }

    render() {
        return (
            <main className="main">
                <Container fluid={true} className="dashboard">
                    <Row>
                        <Col xl="7" lg="6" md="6" sm="12">
                            <Card>
                                <CardBody>
                                    <TimeSelect/>
                                </CardBody>
                            </Card>
                            <Card className="parking-histogram">
                                <CardHeader>{lang.parkingVolumes24H}</CardHeader>
                                <CardBody>
                                    <Bar
                                        data={bar}
                                        options={{
                                            maintainAspectRatio: false,
                                            legend: {display: false},
                                            scales: {yAxes: [{ticks: {min: 0}}]}
                                        }}
                                    />
                                </CardBody>
                            </Card>
                            <Button onClick={() => this.handleStatisticsDownload()} color="primary">
                                {lang.downloadStatistics}
                            </Button>
                        </Col>
                        <Col xl="5" lg="6" md="6" sm="12">
                            <Card>
                                <CardBody>
                                    <RegionSelector/>
                                </CardBody>
                            </Card>
                            <Card className="map-card">
                                <CardBody>
                                    <ParkingRegionsMap/>
                                </CardBody>
                            </Card>
                        </Col>
                    </Row>
                    <Row>
                        <Col>
                            <Card>
                                <CardHeader>
                                    {lang.activeParkings}
                                </CardHeader>
                                <CardBody>
                                    <LastParkingsTable/>
                                </CardBody>
                            </Card>
                        </Col>
                    </Row>
                    <Row>
                        <Col>
                            <Button
                                onClick={this.props.onLogout}
                                color="danger"
                            >
                                <i className="fa fa-sign-out"/>{' '}{lang.signOut}
                            </Button>
                        </Col>
                    </Row>
                    <Row>
                        <Col>
                            <CardGroup>
                                <Card>
                                    <CardBody className="img-center">
                                        <img src={logo} alt="Logo" width="800px" height="104px"/>
                                    </CardBody>
                                </Card>
                            </CardGroup>
                        </Col>
                    </Row>
                </Container>
            </main>
        );
    }
}

function mapStateToProps(state: RootState): Partial<Props> {
    return {
        autoUpdate: state.autoUpdate,
        dateTime: state.dataTime
    };
}

function mapDispatchToProps(dispatch: Dispatch<RootState>): Partial<Props> {
    return {
        onUpdate: () => dispatch(dispatchers.updateData()),
        onLogout: (event: React.MouseEvent<{}>) => dispatch(dispatchers.logout()),
    };
}

const ConnectedDashboard = connect(
    mapStateToProps, mapDispatchToProps)(Dashboard);

export default ConnectedDashboard;
