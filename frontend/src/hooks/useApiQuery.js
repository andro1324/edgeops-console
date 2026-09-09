import { useQuery } from '@tanstack/react-query';

export function useApiQuery(queryKey, queryFn, options = {}) {
  return useQuery({ queryKey, queryFn, ...options });
}