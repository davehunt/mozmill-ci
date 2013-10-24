for ENVIRONMENT in staging production ; do
  echo "Testing patch for $ENVIRONMENT"
  patch --dry-run -p1 <config/$ENVIRONMENT/jenkins.patch || exit $?
done
