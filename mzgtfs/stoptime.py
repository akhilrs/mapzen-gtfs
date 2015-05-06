"""GTFS StopTime entity."""
import entity

class WideTime(object):
  def __init__(self, hours, minutes, seconds):
    assert 0 <= hours
    assert 0 <= minutes <= 60
    assert 0 <= seconds <= 60
    self.hours = hours
    self.minutes = minutes
    self.seconds = seconds
  
  @classmethod
  def from_string(cls, value):
    return cls(*map(int, value.split(':')))

  def __str__(self):
    return ':'.join('%02d'%i for i in list(self))

  def __iter__(self):
    return iter([self.hours, self.minutes, self.seconds])

  def __lt__(self, other):
    return list(self) < list(other)

  def __le__(self, other):
    return list(self) <= list(other)
  
  def __gt__(self, other):
    return list(self) > list(other)
  
  def __ge__(self, other):
    return list(self) >= list(other)
    
  def __eq__(self, other):
    return list(self) == list(other)

class StopTime(entity.Entity):
  """GTFS Stop Time Entity."""
  
  def point(self):
    # Ugly hack.
    return list(self._children)[0].point()

  # Graph
  def stops(self):
    return set(self.children())
    
  def arrive(self):
    if self.get('arrival_time'):
      return WideTime.from_string(self.get('arrival_time'))
    
  def depart(self):
    if self.get('departure_time'):
      return WideTime.from_string(self.get('departure_time'))
    
  def sequence(self):
    return int(self.get('stop_sequence'))  
    
  ##### Validation #####
  def validate(self):
    # Required
    assert self.get('stop_id')
    assert self.get('trip_id')
    assert self.get('stop_sequence')
    if self.get('arrival_time'):
      assert WideTime.from_string(self.get('arrival_time'))
    if self.get('departure_time'):
      assert WideTime.from_string(self.get('departure_time'))
    assert self.arrive() <= self.depart()
    assert self.sequence() >= 0
    # Optional
    if self.get('stop_headsign'):
      pass
    if self.get('pickup_type'):
      assert int(self.get('pickup_type')) in [0,1,2,3]
    if self.get('drop_off_type'):
      assert int(self.get('drop_off_type')) in [0,1,2,3]
    if self.get('shape_dist_traveled'):
      pass
    if self.get('timepoint'):
      assert int(self.get('timepoint')) in [0,1]
      if int(self.get('timepoint')) == 1:
        assert self.arrive()
        assert self.depart()
