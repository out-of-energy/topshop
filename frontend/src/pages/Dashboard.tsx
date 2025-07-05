import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Box,
  Tabs,
  Tab,
  Button,
  CircularProgress,
  Alert,
  Paper,
} from '@mui/material';
import { Add, Refresh } from '@mui/icons-material';
import ShopCard from '../components/ShopCard';
import { shopsApi } from '../services/api';
import { Shop, Region } from '../types/shop';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`region-tabpanel-${index}`}
      aria-labelledby={`region-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const Dashboard: React.FC = () => {
  const [selectedRegion, setSelectedRegion] = useState(0);
  const [shops, setShops] = useState<Shop[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const regions = [
    { value: Region.NORTH_AMERICA, label: 'North America' },
    { value: Region.EUROPE, label: 'Europe' },
    { value: Region.MIDDLE_EAST, label: 'Middle East' },
  ];

  const loadShops = async (region?: Region) => {
    setLoading(true);
    setError(null);
    try {
      const params: any = { size: 20 };
      if (region) {
        params.region = region;
      }
      const response = await shopsApi.getShops(params);
      setShops(response.shops);
    } catch (err) {
      setError('Failed to load shops');
      console.error('Error loading shops:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadShops();
  }, []);

  const handleRegionChange = (event: React.SyntheticEvent, newValue: number) => {
    setSelectedRegion(newValue);
    const region = regions[newValue]?.value;
    if (region) {
      loadShops(region);
    }
  };

  const handleVerifyShopify = async (shopId: number) => {
    try {
      await shopsApi.verifyShopify(shopId);
      // Reload shops to get updated data
      const region = regions[selectedRegion]?.value;
      loadShops(region);
    } catch (err) {
      setError('Failed to verify Shopify');
      console.error('Error verifying Shopify:', err);
    }
  };

  const handleClassifyFashion = async (shopId: number) => {
    try {
      await shopsApi.classifyFashion(shopId);
      // Reload shops to get updated data
      const region = regions[selectedRegion]?.value;
      loadShops(region);
    } catch (err) {
      setError('Failed to classify fashion');
      console.error('Error classifying fashion:', err);
    }
  };

  const handleRefresh = () => {
    const region = regions[selectedRegion]?.value;
    loadShops(region);
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          TopShopE Dashboard
        </Typography>
        <Box>
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={handleRefresh}
            disabled={loading}
            sx={{ mr: 2 }}
          >
            Refresh
          </Button>
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => {/* TODO: Add shop modal */}}
          >
            Add Shop
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Paper sx={{ width: '100%' }}>
        <Tabs
          value={selectedRegion}
          onChange={handleRegionChange}
          aria-label="region tabs"
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          {regions.map((region, index) => (
            <Tab
              key={region.value}
              label={region.label}
              id={`region-tab-${index}`}
              aria-controls={`region-tabpanel-${index}`}
            />
          ))}
        </Tabs>

        {regions.map((region, index) => (
          <TabPanel key={region.value} value={selectedRegion} index={index}>
            {loading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                <CircularProgress />
              </Box>
            ) : shops.length === 0 ? (
              <Box sx={{ textAlign: 'center', p: 4 }}>
                <Typography variant="h6" color="text.secondary">
                  No shops found for {region.label}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                  Try adding some shops or refreshing the data.
                </Typography>
              </Box>
            ) : (
              <Grid container spacing={3}>
                {shops.map((shop) => (
                  <Grid item xs={12} sm={6} md={4} lg={3} key={shop.id}>
                    <ShopCard
                      shop={shop}
                      onVerifyShopify={handleVerifyShopify}
                      onClassifyFashion={handleClassifyFashion}
                    />
                  </Grid>
                ))}
              </Grid>
            )}
          </TabPanel>
        ))}
      </Paper>
    </Container>
  );
};

export default Dashboard; 