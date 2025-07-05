// Utility functions for the frontend
export const formatNumber = (num: number): string => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K';
  }
  return num.toString();
};

export const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString();
};

export const getRegionLabel = (region: string): string => {
  switch (region) {
    case 'north_america':
      return 'North America';
    case 'europe':
      return 'Europe';
    case 'middle_east':
      return 'Middle East';
    default:
      return region;
  }
}; 