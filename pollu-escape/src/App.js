import React from 'react'
import {Helmet} from "react-helmet"
import './App.css';

import { createMuiTheme } from '@material-ui/core/styles'
import { ThemeProvider } from '@material-ui/core/styles'

import Box from '@material-ui/core/Box'
import Grid from '@material-ui/core/Grid'
import AppBar from '@material-ui/core/AppBar'
import Typography from '@material-ui/core/Typography'
import Button from '@material-ui/core/Button'

import Radio from '@material-ui/core/Radio'
import RadioGroup from '@material-ui/core/RadioGroup'
import FormControlLabel from '@material-ui/core/FormControlLabel'

import { makeStyles } from '@material-ui/core/styles'
import logo from './images/logo.png'

const theme = createMuiTheme({
  palette: {
    type: "light",
    primary: {
      main: '#90caf9'
    },
    secondary: {
      main: '#f48fb1'
    },
    error: {
      main: '#f44336'
    },
    warning: {
      main: '#ff9800'
    },
    info: {
      main: '#2196f3'
    },
    success: {
      main: '#4caf50'
    }
  },
})

const useStyles = makeStyles({
  root: {
    maxWidth: "100vw",
  },
  media: {
    height: '6vh',
  }
})

function App() {
  const classes = useStyles()

  const [ dataset_value, set_dataset_value ] = React.useState('http://40.80.159.8/')

  const handle_dataset_change = (event) => {
    set_dataset_value(event.target.value)
  }

  return (
    <Grid>
      <Helmet>
        <title>
          Pollu-Escape
        </title>
      </Helmet>
      <ThemeProvider theme={theme}>
        <Grid container>
          <Grid container item direction='column'>
            <AppBar>
              <Grid container direction='row' >
                <Grid container item md={6} justify='flex-start'>
                  <Box>
                    <img src={logo} alt='logo' className={classes.media}/>
                  </Box>
                  <Box margin={1}>
                    <Typography variant='h4'>
                      Pollu-Escape
                    </Typography>
                  </Box>
                </Grid>
                <Grid container item md={1} justify='flex-end' alignItems='center'>
                  <Box margin={1}>
                    <Typography variant='h6'>
                      Dataset:
                    </Typography>
                  </Box>
                </Grid>
                <Grid container item md={4}>
                  <RadioGroup row value={dataset_value} onChange={handle_dataset_change}>
                      <FormControlLabel value='http://40.80.159.8/' control={<Radio />} label='VOC' />
                      <FormControlLabel value='http://13.88.103.152/' control={<Radio />} label='Temperature' />
                      <FormControlLabel value='http://13.88.96.96/' control={<Radio />} label='Humidity' />
                  </RadioGroup>
                </Grid>
                <Grid container item md={1} justify='flex-end'>
                    <Button fullWidth size='large' color='default'>
                      Login
                    </Button>
                </Grid>
              </Grid>
            </AppBar>
          </Grid>
          <Grid item direction='column' alignItems='stretch'>
            <iframe src={dataset_value} style={{minHeight: '100vh', minWidth: '100vw'}} title='azure_map' />
          </Grid>
        </Grid>
      </ThemeProvider>
    </Grid>
  );
}

export default App;
