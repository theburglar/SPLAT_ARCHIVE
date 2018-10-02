import React from 'react';
import ReactDOM from 'react-dom';
import registerServiceWorker from './app/registerServiceWorker';
import {Provider} from 'react-redux';

import './index.css';
import App from './app/containers/App';
import store from './app/store';

ReactDOM.render(
    <Provider store={store}>
        <App/>
    </Provider>,
    document.getElementById('root'));
registerServiceWorker();
