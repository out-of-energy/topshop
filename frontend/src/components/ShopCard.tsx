import React from 'react';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Chip,
  Button,
  Box,
  Grid,
  Rating,
} from '@mui/material';
import {
  Language,
  ShoppingCart,
  TrendingUp,
  CheckCircle,
  Cancel,
  Help,
} from '@mui/icons-material';
import { Shop, Region } from '../types/shop';

interface ShopCardProps {
  shop: Shop;
  onVerifyShopify?: (id: number) => void;
  onClassifyFashion?: (id: number) => void;
  onViewDetails?: (id: number) => void;
}

const ShopCard: React.FC<ShopCardProps> = ({
  shop,
  onVerifyShopify,
  onClassifyFashion,
  onViewDetails,
}) => {
  const getRegionLabel = (region: Region): string => {
    switch (region) {
      case Region.NORTH_AMERICA:
        return 'North America';
      case Region.EUROPE:
        return 'Europe';
      case Region.MIDDLE_EAST:
        return 'Middle East';
      default:
        return region;
    }
  };

  const getStatusIcon = (isVerified: boolean) => {
    if (isVerified) {
      return <CheckCircle color="success" />;
    }
    return <Cancel color="error" />;
  };

  const getStatusChip = (isVerified: boolean, label: string) => (
    <Chip
      icon={getStatusIcon(isVerified)}
      label={label}
      color={isVerified ? 'success' : 'error'}
      size="small"
      variant="outlined"
    />
  );

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Typography variant="h6" component="h2" gutterBottom>
            {shop.name || shop.domain}
          </Typography>
          <Chip
            label={getRegionLabel(shop.region)}
            size="small"
            color="primary"
            variant="outlined"
          />
        </Box>

        <Typography variant="body2" color="text.secondary" gutterBottom>
          {shop.domain}
        </Typography>

        {shop.description && (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {shop.description}
          </Typography>
        )}

        <Grid container spacing={1} sx={{ mb: 2 }}>
          <Grid item xs={6}>
            {getStatusChip(shop.is_shopify, 'Shopify')}
          </Grid>
          <Grid item xs={6}>
            {getStatusChip(shop.is_womens_fashion, 'Women\'s Fashion')}
          </Grid>
        </Grid>

        {shop.is_womens_fashion && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" color="text.secondary">
              Fashion Confidence: {Math.round(shop.category_confidence * 100)}%
            </Typography>
            <Rating
              value={shop.category_confidence * 5}
              readOnly
              size="small"
              precision={0.1}
            />
          </Box>
        )}

        {shop.overall_score > 0 && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" color="text.secondary">
              Overall Score: {shop.overall_score.toFixed(2)}
            </Typography>
            <Rating
              value={shop.overall_score / 20}
              readOnly
              size="small"
              precision={0.1}
            />
          </Box>
        )}

        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          {shop.traffic_rank && (
            <Chip
              icon={<TrendingUp />}
              label={`Rank: #${shop.traffic_rank}`}
              size="small"
              variant="outlined"
            />
          )}
          {shop.monthly_visits && (
            <Chip
              icon={<TrendingUp />}
              label={`${(shop.monthly_visits / 1000).toFixed(1)}K visits`}
              size="small"
              variant="outlined"
            />
          )}
        </Box>
      </CardContent>

      <CardActions sx={{ justifyContent: 'space-between' }}>
        <Box>
          {!shop.is_shopify && onVerifyShopify && (
            <Button
              size="small"
              startIcon={<Help />}
              onClick={() => onVerifyShopify(shop.id)}
            >
              Verify Shopify
            </Button>
          )}
          {!shop.is_womens_fashion && onClassifyFashion && (
            <Button
              size="small"
              startIcon={<ShoppingCart />}
              onClick={() => onClassifyFashion(shop.id)}
            >
              Classify Fashion
            </Button>
          )}
        </Box>
        <Button
          size="small"
          startIcon={<Language />}
          onClick={() => window.open(`https://${shop.domain}`, '_blank')}
        >
          Visit Site
        </Button>
      </CardActions>
    </Card>
  );
};

export default ShopCard; 